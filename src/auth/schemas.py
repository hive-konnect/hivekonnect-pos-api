from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID    
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
   

    class Config:
        from_attributes = True