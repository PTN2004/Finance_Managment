from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import re
from app.core.database import get_db
from app.models.user import User
from app.core.config import setting

SECRECT_KEY = setting.SECRECT_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES
ACCESS_TOKEN_EXPIRE_DAYS = 7 

# Config password hashing
pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
    bcrypt__rounds=12
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password:str , hashed_password:str) -> bool:
    """Password Authentication"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password:str) -> str:
    """Generate hash for password"""
    return pwd_context.hash(password)


def create_token(data:dict) -> Tuple[str, str]:
    """generate access token and refresh token"""
    to_encode = data.copy()
    
    # Access tokens
    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp" : access_expire,
        "type": "access"
    })
    access_token = jwt.encode(to_encode, key=SECRECT_KEY, algorithm=ALGORITHM)
    
    # Refresh tokens
    refresh_expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp" : refresh_expire,
        "type" : "refresh"
    })
    refresh_token = jwt.encode(to_encode, key=SECRECT_KEY, algorithm=ALGORITHM)
    
    return access_token, refresh_token


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user infomation from the token"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Can't authenticate login infomation",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, key=SECRECT_KEY, algorithms=ALGORITHM)
        phone_number: str = payload.get('sub')
        if phone_number is None:
            raise credentials_exception
        
        # check token type
        token_type: str = payload.get('type')
        if token_type != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token token must access!"
            )
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Token: {str(e)}"
        )
        
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_active(current_user: User=Depends(get_current_user)) -> User:
    if not current_user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active"
        )
        
    return current_user


async def verify_refresh_token(refresh_token:str, 
                               db:Session) -> Tuple[str, User]:
    """Verify refresh token and generate new access token"""
    try:
        payload = jwt.decode(refresh_token, key=SECRECT_KEY, algorithms=ALGORITHM)
        phone_number:str = payload.get('sub')
        
        if phone_number is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Can't authenticate login information",
                headers={"WWW-Authentication" : "Bearer"}
            )
            
        # Check token type
        token_type = payload.get('type')
        if token_type != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token!"
            )
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    
    user = db.query(User).filter(User.phone_number == phone_number).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Can't authenticate login information"
        )
    
    if not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not Active"
        )
        
    access_token, _ = create_token(
        {'sub': user.phone_number}
    )
    
    return access_token, User