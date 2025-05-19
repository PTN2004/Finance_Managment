from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import secrets


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    monthly_income = Column(Float, nullable=True)
    monthly_budget = Column(Float, nullable=True)
    # conservative, moderate, aggressive
    risk_profile = Column(String, nullable=True)

    # Thêm các trường cho xác thực OTP
    otp_secret = Column(String, nullable=True)
    otp_created_at = Column(DateTime(timezone=True), nullable=True)
    is_verified = Column(Boolean, default=False)

    # Quan hệ với các model khác
    budget_plans = relationship("BudgetPlan", back_populates="user")
    spending_goals = relationship("SpendingGoal", back_populates="user")

    def generate_otp(self):
        """Tạo mã OTP 6 chữ số"""
        self.otp_secret = ''.join(
            [str(secrets.randbelow(10)) for _ in range(6)])
        self.otp_created_at = func.now()
        return self.otp_secret

    def verify_otp(self, otp: str) -> bool:
        """Xác thực mã OTP"""
        if not self.otp_secret or not self.otp_created_at:
            return False

        # Kiểm tra OTP có đúng không và còn hạn không (5 phút)
        from datetime import datetime, timedelta, timezone
        if (datetime.now(timezone.utc) - self.otp_created_at) > timedelta(minutes=5):
            print(datetime.now() - self.otp_created_at)
            return False

        return self.otp_secret == otp

    def get_active_budget_plan(self):
        """Lấy kế hoạch ngân sách đang active"""
        from datetime import datetime
        for plan in self.budget_plans:
            if (plan.status == "active" and
                    plan.start_date <= datetime.now() <= plan.end_date):
                return plan
        return None

    def get_active_goals(self):
        """Lấy các mục tiêu đang active"""
        return [goal for goal in self.spending_goals if goal.status == "active"]
