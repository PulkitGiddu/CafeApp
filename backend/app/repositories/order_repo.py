from uuid import UUID
from decimal import Decimal
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem
from app.models.analytics import OrderAnalytics


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(
        self,
        user_id: UUID,
        address_id: UUID,
        total_amount: Decimal,
        payment_method: str,
        notes: Optional[str] = None,
    ) -> Order:
        order = Order(
            user_id=user_id,
            address_id=address_id,
            total_amount=total_amount,
            payment_method=payment_method,
            notes=notes,
            status="PLACED",
            payment_status="PENDING",
        )
        self.db.add(order)
        await self.db.flush()
        return order

    async def create_order_items(
        self, order_id: UUID, items: list[dict]
    ) -> list[OrderItem]:
        """items: list of {product_id, quantity, price}"""
        order_items = []
        for item in items:
            oi = OrderItem(
                order_id=order_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
            )
            self.db.add(oi)
            order_items.append(oi)
        await self.db.flush()
        return order_items

    async def create_analytics(self, order_id: UUID, revenue: Decimal) -> None:
        analytics = OrderAnalytics(order_id=order_id, revenue=revenue)
        self.db.add(analytics)
        await self.db.flush()

    async def get_orders_by_user(self, user_id: UUID) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def get_order_by_id(self, order_id: UUID) -> Optional[Order]:
        result = await self.db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.items),
                selectinload(Order.payment),
                selectinload(Order.address),
            )
        )
        return result.scalar_one_or_none()

    async def update_status(self, order_id: UUID, status: str) -> Optional[Order]:
        result = await self.db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order:
            order.status = status
            await self.db.flush()
        return order

    async def update_payment_status(
        self, order_id: UUID, payment_status: str
    ) -> Optional[Order]:
        result = await self.db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order:
            order.payment_status = payment_status
            await self.db.flush()
        return order

    async def get_all_orders(
        self, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> list[Order]:
        """Admin: list all orders with optional status filter."""
        query = select(Order).options(selectinload(Order.items))
        if status:
            query = query.where(Order.status == status)
        query = query.order_by(Order.created_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().unique().all())
