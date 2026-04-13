from sqlalchemy import Column, DateTime, Integer, String, Boolean, func
from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="Owner")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=  func.now())
    