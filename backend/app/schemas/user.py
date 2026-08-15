from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: UUID
    name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
