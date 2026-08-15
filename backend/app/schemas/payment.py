from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentOut(BaseModel):
    id: UUID
    order_id: UUID
    payment_gateway: Optional[str] = None
    transaction_id: Optional[str] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
