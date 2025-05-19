from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_token, verify_refresh_token

from app.models.user import User
from app.schema.auth import (
    PhoneNumberRequest,
    OTPVerifyRequest,
    OTPResponse,
    TokenResponse,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest
)
from datetime import datetime

router = APIRouter()

@router.post("/request-otp", response_model=OTPResponse)
async def request_otp(request: PhoneNumberRequest, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exists"
        )
        
    otp = user.generate_otp()
    db.commit()
    
    print(f"OTP: {otp}")
    
    return OTPResponse(
        message="Mã OTP đã được gửi đến số điện thoại của bạn",
        expires_in=300
    )
    
    
@router.post("/verify-otp")
async def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exists"
        )
    
    if user.is_verified :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is verify"
        )
    
    if user.verify_otp(request.otp):
        user.is_verified = True
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Verified Successfully"
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="OTP is incorrect"
    )
    

@router.post("/register", response_model=TokenResponse)
async def register_user(request: RegisterRequest, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    user = User(
        phone_number=request.phone_number,
        hashed_password = get_password_hash(request.password),
        full_name=request.full_name
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate access token
    access_token, refresh_token = create_token({"sub" : user.phone_number})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        phone_number=user.phone_number,
        full_name=user.full_name
    )
    

@router.post("/login", response_model=TokenResponse)
async def user_login(request: LoginRequest, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name or password incorrect"
        )
        
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your phone number before logging in"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account has been locked"
        )
        
    access_token, refresh_token = create_token({
        "sub": user.phone_number
    })
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        phone_number=user.phone_number,
        full_name=user.full_name
    )
    
    
@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(request:RefreshTokenRequest, db:Session = Depends(get_db)):
    access_token, user = await verify_refresh_token(request.refresh_token, db)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token,  # Giữ nguyên refresh token
        user_id=user.id,
        phone_number=user.phone_number,
        full_name=user.full_name
    )

    
    
