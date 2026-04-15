from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))

    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False, index=True)

    # Role per shop
    role = Column(String(20), nullable=False, server_default="cashier")

    # Optional override info
    display_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    pin_hash = Column(String, nullable=False)

    is_active = Column(Boolean, server_default=text("true"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    shop = relationship("Shop", back_populates="staff")
