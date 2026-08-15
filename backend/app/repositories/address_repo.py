from uuid import UUID
from typing import Optional

from sqlalchemy import select, update as sa_update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


class AddressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: UUID) -> list[Address]:
        result = await self.db.execute(
            select(Address)
            .where(Address.user_id == user_id)
            .order_by(Address.is_default.desc(), Address.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        result = await self.db.execute(
            select(Address).where(Address.id == address_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, data: AddressCreate) -> Address:
        # If this is set as default, unset other defaults
        if data.is_default:
            await self._unset_defaults(user_id)

        address = Address(user_id=user_id, **data.model_dump())
        self.db.add(address)
        await self.db.flush()
        return address

    async def update(self, address: Address, data: AddressUpdate) -> Address:
        update_data = data.model_dump(exclude_unset=True)
        if update_data.get("is_default"):
            await self._unset_defaults(address.user_id)

        for key, value in update_data.items():
            setattr(address, key, value)
        await self.db.flush()
        return address

    async def delete(self, address_id: UUID) -> None:
        await self.db.execute(
            sa_delete(Address).where(Address.id == address_id)
        )
        await self.db.flush()

    async def _unset_defaults(self, user_id: UUID) -> None:
        await self.db.execute(
            sa_update(Address)
            .where(Address.user_id == user_id, Address.is_default.is_(True))
            .values(is_default=False)
        )
