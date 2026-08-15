from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.models.admin import AdminUser
from app.repositories.order_repo import OrderRepository
from app.schemas.order import OrderOut, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter()


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


@router.post("/login", response_model=AdminToken)
async def admin_login(
    payload: AdminLogin,
    db: AsyncSession = Depends(get_db),
):
    """Admin login with username/password."""
    result = await db.execute(
        select(AdminUser).where(AdminUser.username == payload.username)
    )
    admin = result.scalar_one_or_none()

    if not admin or not verify_password(payload.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        user_id=str(admin.id),
        extra={"role": admin.role},
    )

    return AdminToken(access_token=token, role=admin.role)


@router.get("/orders", response_model=list[OrderOut])
async def list_all_orders(
    status_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    # TODO: Add admin-only auth dependency
):
    """Admin: List all orders with optional status filter."""
    order_repo = OrderRepository(db)
    orders = await order_repo.get_all_orders(
        status=status_filter, limit=limit, offset=offset
    )
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


@router.put("/orders/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: UUID,
    payload: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    # TODO: Add admin-only auth dependency
):
    """Admin: Update order status."""
    service = OrderService(db)
    return await service.update_order_status(order_id, payload.status)
