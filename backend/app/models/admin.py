import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    password: Mapped[Optional[str]] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(50), default="ADMIN")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
