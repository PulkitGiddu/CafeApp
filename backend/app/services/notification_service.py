import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.notification_repo import NotificationRepository

logger = logging.getLogger(__name__)


class NotificationService:
    """Handles push notifications (Firebase) and in-app notification logging."""

    def __init__(self, db: AsyncSession):
        self.notification_repo = NotificationRepository(db)

    async def notify_order_placed(
        self, user_id: UUID, order_id: str, total: float
    ) -> None:
        title = "Order Placed! 🎉"
        message = f"Your order #{order_id[:8]} for ₹{total:.2f} has been placed."

        # Log to DB
        await self.notification_repo.create(user_id, title, message)

        # Send FCM push (stub)
        await self._send_fcm(user_id, title, message)

    async def notify_status_change(
        self, user_id: UUID, order_id: str, status: str
    ) -> None:
        status_messages = {
            "PREPARING": "Your order is being prepared! 👨‍🍳",
            "OUT_FOR_DELIVERY": "Your order is on its way! 🚗",
            "DELIVERED": "Your order has been delivered! Enjoy! 😋",
            "CANCELLED": "Your order has been cancelled. 😔",
        }
        title = f"Order Update"
        message = status_messages.get(
            status, f"Your order #{order_id[:8]} status: {status}"
        )

        await self.notification_repo.create(user_id, title, message)
        await self._send_fcm(user_id, title, message)

    async def _send_fcm(self, user_id: UUID, title: str, body: str) -> None:
        """
        Send Firebase Cloud Messaging push notification.
        TODO: Implement with firebase_admin when FCM tokens are stored.
        """
        logger.info(f"[FCM STUB] → User {user_id}: {title} — {body}")
        # When ready:
        # from firebase_admin import messaging
        # message = messaging.Message(
        #     notification=messaging.Notification(title=title, body=body),
        #     token=user_fcm_token,
        # )
        # messaging.send(message)
