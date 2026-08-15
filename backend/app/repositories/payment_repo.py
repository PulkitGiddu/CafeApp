from uuid import UUID
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        order_id: UUID,
        amount: Decimal,
        payment_gateway: str = "Razorpay",
    ) -> Payment:
        payment = Payment(
            order_id=order_id,
            amount=amount,
            payment_gateway=payment_gateway,
            status="PENDING",
        )
        self.db.add(payment)
        await self.db.flush()
        return payment

    async def get_by_order_id(self, order_id: UUID) -> Optional[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        order_id: UUID,
        status: str,
        transaction_id: Optional[str] = None,
    ) -> Optional[Payment]:
        payment = await self.get_by_order_id(order_id)
        if payment:
            payment.status = status
            if transaction_id:
                payment.transaction_id = transaction_id
            await self.db.flush()
        return payment
