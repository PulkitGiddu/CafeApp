import uuid
from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Numeric, Date, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class OrderAnalytics(Base):
    __tablename__ = "order_analytics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id")
    )
    revenue: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    order_date: Mapped[date] = mapped_column(Date, server_default=func.current_date())

    order: Mapped[Optional["Order"]] = relationship("Order", back_populates="analytics")
