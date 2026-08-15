from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.menu import MenuResponse
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("", response_model=MenuResponse)
async def get_menu(db: AsyncSession = Depends(get_db)):
    """Get full menu with categories and products."""
    service = MenuService(db)
    return await service.get_menu()
