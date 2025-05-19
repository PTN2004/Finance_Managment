import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List
import secrets
load_dotenv()

class Setting(BaseSettings):
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "phamtu")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "522004")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "finance_agent")
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # Security
    SECRECT_KEY: str = os.getenv("SECRECT_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    CORS_setting: List = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
setting = Setting()