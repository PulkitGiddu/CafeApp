from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import OTPRequest, OTPVerify, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/send-otp", response_model=dict)
async def send_otp(
    payload: OTPRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send OTP to the provided phone number."""
    service = AuthService(db)
    return await service.send_otp(payload.phone)


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(
    payload: OTPVerify,
    db: AsyncSession = Depends(get_db),
):
    """Verify OTP and return JWT token. Creates user if first login."""
    service = AuthService(db)
    try:
        result = await service.verify_otp(payload.phone, payload.otp)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
