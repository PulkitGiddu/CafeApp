from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field


# ---------- Request ----------

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    address_id: UUID
    payment_method: str = Field(..., examples=["UPI", "CARD", "COD"])
    notes: Optional[str] = None
    items: list[OrderItemCreate] = Field(..., min_length=1)


# ---------- Response ----------

class OrderItemOut(BaseModel):
    id: UUID
    product_id: UUID
    product_name: Optional[str] = None
    quantity: int
    price: Decimal

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: UUID
    status: str
    payment_status: str
    payment_method: Optional[str] = None
    total_amount: Decimal
    notes: Optional[str] = None
    items_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderDetailOut(BaseModel):
    id: UUID
    status: str
    payment_status: str
    payment_method: Optional[str] = None
    total_amount: Decimal
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}


class OrderCreateResponse(BaseModel):
    order_id: UUID
    total_amount: Decimal
    status: str
    payment_status: str
    razorpay: Optional[dict] = None


class OrderStatusUpdate(BaseModel):
    status: str = Field(
        ...,
        examples=["PLACED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"],
    )
