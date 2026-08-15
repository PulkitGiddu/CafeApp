import logging
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.order_repo import OrderRepository
from app.repositories.menu_repo import MenuRepository
from app.repositories.address_repo import AddressRepository
from app.repositories.payment_repo import PaymentRepository
from app.schemas.order import (
    OrderCreate,
    OrderCreateResponse,
    OrderDetailOut,
    OrderItemOut,
    OrderOut,
)
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.services.whatsapp_service import WhatsAppService

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.menu_repo = MenuRepository(db)
        self.address_repo = AddressRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.payment_service = PaymentService()
        self.notification_service = NotificationService(db)
        self.whatsapp_service = WhatsAppService()

    async def create_order(
        self, user_id: UUID, data: OrderCreate
    ) -> OrderCreateResponse:
        """
        CRITICAL ORDER FLOW:
        1. Validate address belongs to user
        2. Fetch product prices from DB (NEVER trust frontend)
        3. Calculate total_amount server-side
        4. Create order + order_items
        5. Create Razorpay order
        6. Create payment record
        7. Send WhatsApp to owner
        8. Send push notification
        """

        # 1. Validate address
        address = await self.address_repo.get_by_id(data.address_id)
        if not address or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid address",
            )

        # 2. Fetch product prices from DB
        product_ids = [item.product_id for item in data.items]
        products = await self.menu_repo.get_products_by_ids(product_ids)
        product_map = {p.id: p for p in products}

        # Validate all products exist and are available
        for item in data.items:
            product = product_map.get(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {item.product_id} not found",
                )
            if not product.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product '{product.name}' is currently unavailable",
                )

        # 3. Calculate total server-side
        total_amount = Decimal("0.00")
        order_items_data = []
        for item in data.items:
            product = product_map[item.product_id]
            item_total = product.price * item.quantity
            total_amount += item_total
            order_items_data.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": product.price,
                }
            )

        # 4. Create order
        order = await self.order_repo.create_order(
            user_id=user_id,
            address_id=data.address_id,
            total_amount=total_amount,
            payment_method=data.payment_method,
            notes=data.notes,
        )

        # 5. Create order items
        await self.order_repo.create_order_items(order.id, order_items_data)

        # 6. Create analytics record
        await self.order_repo.create_analytics(order.id, total_amount)

        # 7. Handle payment
        razorpay_data = None
        if data.payment_method != "COD":
            try:
                razorpay_data = self.payment_service.create_razorpay_order(
                    amount=total_amount,
                    order_id=str(order.id),
                )
            except Exception as e:
                logger.error(f"Razorpay order creation failed: {e}")
                # Continue without Razorpay for now

        # 8. Create payment record
        await self.payment_repo.create(
            order_id=order.id,
            amount=total_amount,
            payment_gateway="Razorpay" if data.payment_method != "COD" else "COD",
        )

        # 9. Send WhatsApp to cafe owner (fire-and-forget)
        try:
            product_names = [
                f"{product_map[i.product_id].name} x{i.quantity}"
                for i in data.items
            ]
            await self.whatsapp_service.send_order_to_owner(
                order_id=str(order.id),
                items=product_names,
                total=float(total_amount),
            )
        except Exception as e:
            logger.warning(f"WhatsApp notification failed: {e}")

        # 10. Send push notification (fire-and-forget)
        try:
            await self.notification_service.notify_order_placed(
                user_id=user_id, order_id=str(order.id), total=float(total_amount)
            )
        except Exception as e:
            logger.warning(f"Push notification failed: {e}")

        return OrderCreateResponse(
            order_id=order.id,
            total_amount=total_amount,
            status=order.status,
            payment_status=order.payment_status,
            razorpay=razorpay_data,
        )

    async def get_user_orders(self, user_id: UUID) -> list[OrderOut]:
        orders = await self.order_repo.get_orders_by_user(user_id)
        result = []
        for o in orders:
            result.append(
                OrderOut(
                    id=o.id,
                    status=o.status,
                    payment_status=o.payment_status,
                    payment_method=o.payment_method,
                    total_amount=o.total_amount,
                    notes=o.notes,
                    items_count=len(o.items),
                    created_at=o.created_at,
                    updated_at=o.updated_at,
                )
            )
        return result

    async def get_order_detail(self, order_id: UUID, user_id: UUID) -> OrderDetailOut:
        order = await self.order_repo.get_order_by_id(order_id)
        if not order or order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        items = []
        for oi in order.items:
            items.append(
                OrderItemOut(
                    id=oi.id,
                    product_id=oi.product_id,
                    product_name=oi.product.name if oi.product else None,
                    quantity=oi.quantity,
                    price=oi.price,
                )
            )
        return OrderDetailOut(
            id=order.id,
            status=order.status,
            payment_status=order.payment_status,
            payment_method=order.payment_method,
            total_amount=order.total_amount,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=items,
        )

    async def update_order_status(self, order_id: UUID, new_status: str) -> OrderOut:
        """Admin: update order status and send notification."""
        valid_statuses = {"PLACED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"}
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {valid_statuses}",
            )

        order = await self.order_repo.update_status(order_id, new_status)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Notify user of status change
        try:
            await self.notification_service.notify_status_change(
                user_id=order.user_id,
                order_id=str(order_id),
                status=new_status,
            )
        except Exception as e:
            logger.warning(f"Notification failed: {e}")

        return OrderOut(
            id=order.id,
            status=order.status,
            payment_status=order.payment_status,
            payment_method=order.payment_method,
            total_amount=order.total_amount,
            notes=order.notes,
            items_count=0,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
