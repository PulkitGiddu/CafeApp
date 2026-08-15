import logging
from decimal import Decimal

import razorpay

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PaymentService:
    def __init__(self):
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            self.client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
        else:
            self.client = None
            logger.warning("Razorpay credentials not configured — payment mock mode")

    def create_razorpay_order(self, amount: Decimal, order_id: str) -> dict:
        """Create a Razorpay order. Amount is in INR, Razorpay expects paise."""
        amount_paise = int(amount * 100)

        if not self.client:
            # Mock mode
            logger.info(f"[MOCK RAZORPAY] Order {order_id}, amount: {amount_paise} paise")
            return {
                "order_id": f"order_mock_{order_id[:8]}",
                "amount": amount_paise,
                "currency": "INR",
                "key": settings.RAZORPAY_KEY_ID or "rzp_test_mock",
            }

        rz_order = self.client.order.create(
            data={
                "amount": amount_paise,
                "currency": "INR",
                "receipt": order_id,
                "notes": {"arthcafe_order_id": order_id},
            }
        )

        return {
            "order_id": rz_order["id"],
            "amount": rz_order["amount"],
            "currency": rz_order["currency"],
            "key": settings.RAZORPAY_KEY_ID,
        }

    def verify_payment_signature(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> bool:
        """Verify Razorpay payment signature."""
        if not self.client:
            # Mock mode — always succeed
            logger.info("[MOCK RAZORPAY] Payment verified (mock)")
            return True

        try:
            self.client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )
            return True
        except razorpay.errors.SignatureVerificationError:
            return False
