from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from typing import Optional, Type

from app.models.transaction import Transaction, TransactionCategory, TransactionType
from app.core.database import get_db


class RecordTransactionInput(BaseModel):
    description: str = Field(..., description="Mô tả giao dịch, ví dụ: Mua cà phê, Nhận lương")
    amount: float = Field(..., description="Số tiền của giao dịch")
    category: str = Field(..., description="Danh mục giao dịch, ví dụ: Ăn uống, Lương, Giải trí")
    type: str = Field(..., description="Loại giao dịch: income hoặc expense. Hãy suy luận nếu không rõ.")
    
    # Các trường không bắt buộc
    payment_method: Optional[str] = Field(None, description="Phương thức thanh toán nếu người dùng cung cấp (ví dụ: Tiền mặt, Momo)")
    location: Optional[str] = Field(None, description="Địa điểm nếu có (ví dụ: Highland Coffee, Vincom Bà Triệu)")


class RecordTransactionTool(BaseTool):
    name:str = "record_transaction"
    description:str = """Ghi lại chi tiêu hoặc thu nhập của người dùng"""
    args_schema: Type[BaseModel] = RecordTransactionInput
    return_direct:bool = True
    user_id:int
    def _run(self, description: str, amount: float, category: str,  type: str, payment_method: str = None, location:str = None) -> str:
       
        db = next(get_db())
        try:
            print("✅ GOI HAM RECORD")    
            transaction = Transaction(
                user_id = self.user_id,
                description=description,
                amount=amount,
                category=category,
                type=type,
                payment_method=payment_method,
                location=location
            )
            db.add(transaction)
            db.commit()
            db.refresh()
            return "✅ Đã ghi nhận giao dịch thành công!  💸 {description} - {amount:,.0f}đ"
        except Exception as e:
            db.rollback()
            return f"Đã xảy ra lỗi khi ghi nhận giao dịch: {str(e)}"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Tool này không hỗ trợ chạy bất đồng bộ.")

