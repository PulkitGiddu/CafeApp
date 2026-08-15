"""
ArthCafe — Seed Data Script
Run: python -m seed
Populates the database with sample categories, products, and an admin user.
"""

import asyncio
import uuid

from sqlalchemy import text
from app.core.security import hash_password
from app.db.session import async_session


CATEGORIES = [
    {
        "name": "Hot Beverages",
        "description": "Freshly brewed hot drinks",
        "products": [
            {"name": "Cappuccino", "description": "Rich espresso with steamed milk foam", "price": 180.00, "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400"},
            {"name": "Latte", "description": "Smooth espresso with velvety steamed milk", "price": 200.00, "image_url": "https://images.unsplash.com/photo-1561882468-9110e9e0e536?w=400"},
            {"name": "Americano", "description": "Bold espresso diluted with hot water", "price": 150.00, "image_url": "https://images.unsplash.com/photo-1551030173-122aabc4489c?w=400"},
            {"name": "Masala Chai", "description": "Traditional Indian spiced tea", "price": 80.00, "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"},
            {"name": "Hot Chocolate", "description": "Rich and creamy chocolate drink", "price": 220.00, "image_url": "https://images.unsplash.com/photo-1517578239113-b03992dcdd25?w=400"},
        ],
    },
    {
        "name": "Cold Beverages",
        "description": "Refreshing cold drinks",
        "products": [
            {"name": "Iced Coffee", "description": "Chilled coffee with ice and milk", "price": 200.00, "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400"},
            {"name": "Cold Brew", "description": "Slow-steeped cold coffee concentrate", "price": 250.00, "image_url": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400"},
            {"name": "Mango Smoothie", "description": "Fresh mango blended with yogurt", "price": 180.00, "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=400"},
            {"name": "Fresh Lime Soda", "description": "Sparkling lime with mint", "price": 120.00, "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed514?w=400"},
        ],
    },
    {
        "name": "Snacks",
        "description": "Light bites and quick eats",
        "products": [
            {"name": "Veg Sandwich", "description": "Grilled sandwich with fresh vegetables", "price": 150.00, "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400"},
            {"name": "Paneer Wrap", "description": "Tandoori paneer in a soft wrap", "price": 180.00, "image_url": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400"},
            {"name": "French Fries", "description": "Crispy golden fries with dip", "price": 120.00, "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400"},
            {"name": "Garlic Bread", "description": "Toasted bread with garlic butter", "price": 130.00, "image_url": "https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=400"},
        ],
    },
    {
        "name": "Desserts",
        "description": "Sweet treats to end your meal",
        "products": [
            {"name": "Chocolate Brownie", "description": "Warm, fudgy brownie with a scoop of ice cream", "price": 200.00, "image_url": "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=400"},
            {"name": "Cheesecake", "description": "Creamy New York style cheesecake", "price": 250.00, "image_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400"},
            {"name": "Gulab Jamun", "description": "Soft, warm milk-solid dumplings in syrup", "price": 100.00, "image_url": "https://images.unsplash.com/photo-1666190050103-e44a193114e1?w=400"},
        ],
    },
]


async def seed():
    async with async_session() as session:
        # Check if data already exists
        result = await session.execute(text("SELECT COUNT(*) FROM categories"))
        count = result.scalar()
        if count and count > 0:
            print("⚠️  Database already has categories. Skipping seed.")
            return

        print("🌱 Seeding ArthCafe database...")

        # Seed categories and products
        for cat_data in CATEGORIES:
            cat_id = uuid.uuid4()
            await session.execute(
                text(
                    "INSERT INTO categories (id, name, description) VALUES (:id, :name, :desc)"
                ),
                {"id": cat_id, "name": cat_data["name"], "desc": cat_data["description"]},
            )

            for prod in cat_data["products"]:
                await session.execute(
                    text(
                        "INSERT INTO products (id, category_id, name, description, price, image_url) "
                        "VALUES (:id, :cat_id, :name, :desc, :price, :image_url)"
                    ),
                    {
                        "id": uuid.uuid4(),
                        "cat_id": cat_id,
                        "name": prod["name"],
                        "desc": prod["description"],
                        "price": prod["price"],
                        "image_url": prod["image_url"],
                    },
                )
            print(f"  ✅ {cat_data['name']} — {len(cat_data['products'])} products")

        # Seed admin user (username: admin, password: admin123)
        admin_id = uuid.uuid4()
        hashed = hash_password("admin123")
        await session.execute(
            text(
                "INSERT INTO admin_users (id, username, password, role) "
                "VALUES (:id, :username, :password, :role)"
            ),
            {"id": admin_id, "username": "admin", "password": hashed, "role": "ADMIN"},
        )
        print("  ✅ Admin user created (admin / admin123)")

        await session.commit()
        print("\n🎉 Seed complete!")


if __name__ == "__main__":
    asyncio.run(seed())
