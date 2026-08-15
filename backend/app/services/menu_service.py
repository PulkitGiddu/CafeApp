from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.menu_repo import MenuRepository
from app.schemas.menu import CategoryWithProducts, MenuResponse, ProductOut


class MenuService:
    def __init__(self, db: AsyncSession):
        self.menu_repo = MenuRepository(db)

    async def get_menu(self) -> MenuResponse:
        """Get full menu grouped by categories."""
        categories = await self.menu_repo.get_full_menu()

        result = []
        for cat in categories:
            products = [
                ProductOut.model_validate(p)
                for p in cat.products
                if p.is_available
            ]
            result.append(
                CategoryWithProducts(
                    id=cat.id,
                    name=cat.name,
                    description=cat.description,
                    products=products,
                )
            )

        return MenuResponse(categories=result)
