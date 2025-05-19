from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import setting

# Create Sqlalchemy engine
print(setting.SQLALCHEMY_DATABASE_URI)
engine = create_engine(setting.SQLALCHEMY_DATABASE_URI)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
def init_db():
    """Initialize database with all models"""
    from app.models.user import User
    from app.models.transaction import Transaction
    from app.models.budget import BudgetPlan
    
    Base.metadata.create_all(bind=engine)