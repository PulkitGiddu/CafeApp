from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# Naming convention for constraints (Alembic-friendly)
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata


# Import all models so they register with Base.metadata
from app.models.user import User  # noqa: F401, E402
from app.models.address import Address  # noqa: F401, E402
from app.models.category import Category  # noqa: F401, E402
from app.models.product import Product  # noqa: F401, E402
from app.models.cart import Cart, CartItem  # noqa: F401, E402
from app.models.order import Order, OrderItem  # noqa: F401, E402
from app.models.payment import Payment  # noqa: F401, E402
from app.models.delivery import DeliveryAgent, OrderDelivery  # noqa: F401, E402
from app.models.admin import AdminUser  # noqa: F401, E402
from app.models.notification import Notification  # noqa: F401, E402
from app.models.analytics import OrderAnalytics  # noqa: F401, E402
