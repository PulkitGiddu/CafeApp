from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.address_repo import AddressRepository
from app.schemas.address import AddressCreate, AddressUpdate, AddressOut


class AddressService:
    def __init__(self, db: AsyncSession):
        self.address_repo = AddressRepository(db)

    async def list_addresses(self, user_id: UUID) -> list[AddressOut]:
        addresses = await self.address_repo.list_by_user(user_id)
        return [AddressOut.model_validate(a) for a in addresses]

    async def create_address(self, user_id: UUID, data: AddressCreate) -> AddressOut:
        address = await self.address_repo.create(user_id, data)
        return AddressOut.model_validate(address)

    async def update_address(
        self, user_id: UUID, address_id: UUID, data: AddressUpdate
    ) -> AddressOut:
        address = await self.address_repo.get_by_id(address_id)
        if not address or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
        updated = await self.address_repo.update(address, data)
        return AddressOut.model_validate(updated)

    async def delete_address(self, user_id: UUID, address_id: UUID) -> None:
        address = await self.address_repo.get_by_id(address_id)
        if not address or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
        await self.address_repo.delete(address_id)
