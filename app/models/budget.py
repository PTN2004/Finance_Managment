from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class BudgetPlan(Base):
    __tablename__ = "budget_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)  # Tên kế hoạch (ví dụ: "Kế hoạch tháng 3/2024")
    monthly_income = Column(Float)
    total_budget = Column(Float)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    status = Column(String)  # active, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Quan hệ
    user = relationship("User", back_populates="budget_plans")
    categories = relationship("BudgetCategory", back_populates="budget_plan")

    def calculate_remaining_budget(self):
        """Tính toán ngân sách còn lại"""
        allocated = sum(
            category.allocated_amount for category in self.categories)
        return self.total_budget - allocated


class BudgetCategory(Base):
    __tablename__ = "budget_categories"

    id = Column(Integer, primary_key=True, index=True)
    budget_plan_id = Column(Integer, ForeignKey("budget_plans.id"))
    category_name = Column(String)  # Ví dụ: Ăn uống, Di chuyển, Giải trí...
    allocated_amount = Column(Float)  # Số tiền được phân bổ
    spent_amount = Column(Float, default=0)  # Số tiền đã chi
    percentage = Column(Float)  # Phần trăm của tổng ngân sách
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Quan hệ
    budget_plan = relationship("BudgetPlan", back_populates="categories")

    def calculate_remaining(self):
        """Tính toán số tiền còn lại trong danh mục"""
        return self.allocated_amount - self.spent_amount

    def calculate_usage_percentage(self):
        """Tính toán phần trăm đã sử dụng"""
        if self.allocated_amount == 0:
            return 0
        return (self.spent_amount / self.allocated_amount) * 100


class SpendingGoal(Base):
    __tablename__ = "spending_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)  # Tên mục tiêu
    target_amount = Column(Float)  # Số tiền mục tiêu
    current_amount = Column(Float, default=0)  # Số tiền hiện tại
    start_date = Column(DateTime(timezone=True))
    target_date = Column(DateTime(timezone=True))
    status = Column(String)  # active, completed, cancelled
    category = Column(String)  # Loại mục tiêu (tiết kiệm, đầu tư...)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Quan hệ
    user = relationship("User", back_populates="spending_goals")

    def calculate_progress(self):
        """Tính toán tiến độ đạt được mục tiêu"""
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def calculate_remaining_days(self):
        """Tính số ngày còn lại để đạt mục tiêu"""
        from datetime import datetime
        if not self.target_date:
            return None
        remaining = self.target_date - datetime.now()
        return remaining.days
