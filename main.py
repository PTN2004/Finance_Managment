from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import setting
from app.core.database import init_db
from app.api.v1.auth import router
from app.api.v1.api import api_router

app = FastAPI(
    title="AI Finance Agent",
    description="AI-powered personal finance management system",
    version="1.0.0"
)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.CORS_setting,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1/auth")
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to AI Finance Agent API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

