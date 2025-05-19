from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from datetime import datetime


class GoalInput(BaseModel):
    name: str = Field(..., description="Tên mục tiêu")
    target_amount: float = Field(..., description="Số tiền mục tiêu")
    deadline: datetime = Field(..., description="Thời hạn đạt mục tiêu")
    category: Optional[str] = Field(
        None, description="Danh mục chi tiêu liên quan")


class GoalTool(BaseTool):
    name = "manage_goal"
    description = "Tạo và theo dõi mục tiêu chi tiêu"
    args_schema: Type[BaseModel] = GoalInput
    return_direct = True

    def _run(self, name: str, target_amount: float, deadline: datetime, category: Optional[str] = None) -> str:
        try:
            # TODO: Implement actual goal management logic
            return f"Đã tạo mục tiêu {name} với số tiền {target_amount:,.0f} VND, hạn chót {deadline.strftime('%d/%m/%Y')}"
        except Exception as e:
            return f"Lỗi khi quản lý mục tiêu: {str(e)}"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Tool này không hỗ trợ chạy bất đồng bộ.")
