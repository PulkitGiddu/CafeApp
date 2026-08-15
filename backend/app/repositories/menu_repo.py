from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.product import Product


class MenuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_full_menu(self) -> list[Category]:
        """Fetch active categories with their available products (eager-loaded)."""
        result = await self.db.execute(
            select(Category)
            .where(Category.is_active.is_(True))
            .options(
                selectinload(Category.products.and_(Product.is_available.is_(True)))
            )
            .order_by(Category.name)
        )
        return list(result.scalars().unique().all())

    async def get_product_by_id(self, product_id):
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_products_by_ids(self, product_ids: list) -> list[Product]:
        result = await self.db.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        return list(result.scalars().all())
