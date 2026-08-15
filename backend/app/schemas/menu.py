from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class ProductOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    is_available: bool

    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    is_active: bool

    model_config = {"from_attributes": True}


class CategoryWithProducts(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    products: list[ProductOut]

    model_config = {"from_attributes": True}


class MenuResponse(BaseModel):
    categories: list[CategoryWithProducts]
