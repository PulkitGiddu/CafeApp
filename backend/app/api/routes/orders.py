from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_id
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderCreateResponse, OrderDetailOut, OrderOut
from app.services.order_service import OrderService

router = APIRouter()


@router.post("", response_model=OrderCreateResponse, status_code=201)
async def create_order(
    payload: OrderCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new order (full order flow)."""
    service = OrderService(db)
    return await service.create_order(user_id, payload)


@router.get("", response_model=list[OrderOut])
async def list_orders(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all orders for the current user."""
    service = OrderService(db)
    return await service.get_user_orders(user_id)


@router.get("/{order_id}", response_model=OrderDetailOut)
async def get_order_detail(
    order_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed info for a specific order."""
    service = OrderService(db)
    return await service.get_order_detail(order_id, user_id)
