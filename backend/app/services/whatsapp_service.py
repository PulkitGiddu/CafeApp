import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class WhatsAppService:
    """
    Sends order details to the cafe owner via WhatsApp.
    Currently a mock implementation — replace with Twilio or Meta WhatsApp API.
    """

    async def send_order_to_owner(
        self, order_id: str, items: list[str], total: float
    ) -> None:
        items_text = "\n".join(f"  • {item}" for item in items)
        message = (
            f"🧾 *New Order #{order_id[:8]}*\n\n"
            f"{items_text}\n\n"
            f"💰 Total: ₹{total:.2f}\n\n"
            f"Please prepare the order!"
        )

        owner_phone = settings.CAFE_OWNER_PHONE

        if settings.WHATSAPP_API_URL and settings.WHATSAPP_API_KEY:
            # Real WhatsApp API call
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.WHATSAPP_API_URL,
                    headers={"Authorization": f"Bearer {settings.WHATSAPP_API_KEY}"},
                    json={
                        "messaging_product": "whatsapp",
                        "to": owner_phone,
                        "type": "text",
                        "text": {"body": message},
                    },
                )
                logger.info(f"[WhatsApp] Sent to {owner_phone}: {response.status_code}")
        else:
            # Mock mode
            logger.info(
                f"[WHATSAPP MOCK] → {owner_phone}\n{message}"
            )
