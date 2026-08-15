from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_id
from app.db.session import get_db
from app.schemas.address import AddressCreate, AddressOut, AddressUpdate
from app.services.address_service import AddressService

router = APIRouter()


@router.get("", response_model=list[AddressOut])
async def list_addresses(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all addresses for the current user."""
    service = AddressService(db)
    return await service.list_addresses(user_id)


@router.post("", response_model=AddressOut, status_code=201)
async def create_address(
    payload: AddressCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Add a new address."""
    service = AddressService(db)
    return await service.create_address(user_id, payload)


@router.put("/{address_id}", response_model=AddressOut)
async def update_address(
    address_id: UUID,
    payload: AddressUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing address."""
    service = AddressService(db)
    return await service.update_address(user_id, address_id, payload)


@router.delete("/{address_id}", status_code=204)
async def delete_address(
    address_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete an address."""
    service = AddressService(db)
    await service.delete_address(user_id, address_id)
