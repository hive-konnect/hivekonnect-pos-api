from sqlalchemy import Column, String, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Shop(Base):
    __tablename__ = "shops"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    shop_name = Column(String(255), nullable=False)
    shop_type = Column(String(100), server_default="General")
    
    description = Column(String(500))
    address = Column(String(255))
    business_phone_number = Column(String(20))
    
    currency = Column(String(10), server_default="UGX")

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="shops")
    staff = relationship("Staff", back_populates="shop", cascade="all, delete-orphan")