from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class PinLoginRequest(BaseModel):
    shop_id: UUID
    pin: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseModel):
    message: str


class OwnerTokenPayload(BaseModel):
    type: Literal["owner"]
    user_id: UUID
    shop_id: None = None


class StaffTokenPayload(BaseModel):
    type: Literal["staff"]
    staff_id: UUID
    shop_id: UUID
    role: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID    
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
   

    class Config:
        from_attributes = True
