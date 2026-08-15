from pydantic import BaseModel, Field


class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, examples=["+919876543210"])


class OTPVerify(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, examples=["+919876543210"])
    otp: str = Field(..., min_length=4, max_length=6, examples=["123456"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    is_new_user: bool
