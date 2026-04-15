from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class StaffCreate(BaseModel):
    display_name: str = Field(..., max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    role: Literal["cashier", "manager"] = "cashier"


class StaffResponse(BaseModel):
    id: UUID
    shop_id: UUID
    role: str
    display_name: str | None = None
    phone: str | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class StaffCreateResponse(BaseModel):
    staff: StaffResponse
    pin: str


class StaffPinResetResponse(BaseModel):
    staff_id: UUID
    pin: str