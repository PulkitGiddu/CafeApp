from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    address_line: str = Field(..., min_length=1)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_default: bool = False


class AddressUpdate(BaseModel):
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_default: Optional[bool] = None


class AddressOut(BaseModel):
    id: UUID
    user_id: UUID
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_default: bool
    created_at: datetime

    model_config = {"from_attributes": True}
