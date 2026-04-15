from sqlalchemy import Boolean, Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)

    username = Column(String(255), unique=True, index=True, nullable=True)  # Optional username field
    
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    shops = relationship("Shop", back_populates="owner", cascade="all, delete-orphan")
