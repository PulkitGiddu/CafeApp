from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_id
from app.db.session import get_db


async def get_db_session(db: AsyncSession = Depends(get_db)):
    """Alias dependency for DB session."""
    return db


async def get_authenticated_user(
    user_id: UUID = Depends(get_current_user_id),
) -> UUID:
    """Alias dependency for authenticated user ID."""
    return user_id
