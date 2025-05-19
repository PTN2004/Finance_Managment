from pydantic import BaseModel, Field, validator
import re

class PhoneNumberRequest(BaseModel):
    phone_number: str = Field(..., description="The phone number of the user")
    
    @validator('phone_number')
    def validator_phone_number(cls, v):
        if not re.match(r'^(\+84|0)[3|5|7|8|9][0-9]{8}$', v):
            raise ValueError("Phone Number Invalid")
        return v
        
class OTPVerifyRequest(BaseModel):
    phone_number: str
    otp: str = Field(..., min_length=6, max_length=6)
    @validator('otp')
    def validate_otp(cls, v):
        if not v.isdigit():
            raise ValueError('OTP phải là số')
        return v


class RegisterRequest(BaseModel):
    phone_number: str
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not re.match(r'^(\+84|0)[3|5|7|8|9][0-9]{8}$', v):
            raise ValueError('Số điện thoại không hợp lệ')
        return v


class LoginRequest(BaseModel):
    phone_number: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    phone_number: str
    full_name: str


class OTPResponse(BaseModel):
    message: str
    expires_in: int = 300  # 5 phút
    
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str