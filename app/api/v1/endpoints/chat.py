from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel

from app.core.agent import FinanceAgent
from app.core.security import get_current_user
from app.models.user import User


class ChatMessage(BaseModel):
    message: str


router = APIRouter()
agent_cache = {}


@router.post("/chat-agent")
async def chat_agent(
    request: ChatMessage,
    user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    try:
        print(f"NAME: {user.full_name} - {user.id}")
        
        # Giữ agent theo user_id
        if user.id not in agent_cache:
            agent_cache[user.id] = FinanceAgent(user.id)
        agent = agent_cache[user.id]
        response = agent.proccess_message(request.message, user.id)
        return {
            "status": "success",
            "data": response
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
