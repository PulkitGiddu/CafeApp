import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_access_token
from app.repositories.user_repo import UserRepository

logger = logging.getLogger(__name__)
settings = get_settings()

# In-memory OTP store (replace with Redis in production)
_otp_store: dict[str, str] = {}


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def send_otp(self, phone: str) -> dict:
        """Generate and 'send' an OTP to the given phone number."""
        if settings.OTP_MOCK:
            otp = settings.OTP_MOCK_CODE
            logger.info(f"[MOCK OTP] {phone} → {otp}")
        else:
            # TODO: Integrate real OTP provider (Twilio / MSG91)
            import random
            otp = str(random.randint(100000, 999999))
            logger.info(f"[OTP] Sending {otp} to {phone}")

        _otp_store[phone] = otp
        return {"message": "OTP sent successfully", "phone": phone}

    async def verify_otp(self, phone: str, otp: str) -> dict:
        """Verify OTP, create user if new, return JWT."""
        stored_otp = _otp_store.get(phone)

        if not stored_otp or stored_otp != otp:
            raise ValueError("Invalid OTP")

        # Clear used OTP
        _otp_store.pop(phone, None)

        # Find or create user
        is_new = False
        user = await self.user_repo.get_by_phone(phone)
        if not user:
            user = await self.user_repo.create(phone=phone)
            is_new = True

        # Generate JWT
        token = create_access_token(user_id=str(user.id))

        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "is_new_user": is_new,
        }
