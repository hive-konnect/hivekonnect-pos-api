from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))

    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Role per shop
    role = Column(String(20), nullable=False, server_default="cashier")

    # Optional override info
    display_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)

    is_active = Column(Boolean, server_default=text("true"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('shop_id', 'user_id', name='unique_shop_user'),
    )

    # Relationships
    shop = relationship("Shop", back_populates="staff")
    user = relationship("User", back_populates="staff_memberships")