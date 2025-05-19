from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type


class BudgetInput(BaseModel):
    category: str = Field(..., description="Danh mục chi tiêu")
    amount: float = Field(..., description="Số tiền ngân sách")
    period: str = Field(..., description="Kỳ hạn ngân sách (tháng/quý/năm)")


class BudgetTool(BaseTool):
    name = "manage_budget"
    description = "Tạo và quản lý ngân sách cho các danh mục chi tiêu"
    args_schema: Type[BaseModel] = BudgetInput
    return_direct = True

    def _run(self, category: str, amount: float, period: str) -> str:
        try:
            # TODO: Implement actual budget management logic
            return f"Đã tạo ngân sách {amount:,.0f} VND cho danh mục {category} trong kỳ {period}"
        except Exception as e:
            return f"Lỗi khi quản lý ngân sách: {str(e)}"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Tool này không hỗ trợ chạy bất đồng bộ.")
