import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Shop(Base):
    __tablename__ = "shops"

    # Identity
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    shop_name = Column(String(255), nullable=False)
    
    # Simple Category (Boutique, Electronics, Pharmacy, General Store, etc.)
    shop_type = Column(String(100), nullable=False, server_default="General")
    
    # Business Details
    description = Column(String(500), nullable=True)
    address = Column(String(255), nullable=True)
    business_phone_number = Column(String(20), nullable=True)
    
    # Financial Basics
    currency = Column(String(10), server_default="UGX")
        
    # Metadata
    owner_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="shops")