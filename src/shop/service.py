from pydantic import BaseModel, Field
from uuid import UUID

class ShopCreate(BaseModel):
    shop_name: str = Field(..., max_length=255)
    shop_type: str = Field("General", max_length=100)
    description: str = Field(None, max_length=500)
    address: str = Field(None, max_length=255)
    business_phone_number: str = Field(None, max_length=20)
    currency: str = Field("UGX", max_length=10)

class ShopResponse(BaseModel):
    
    shop_name: str
    shop_type: str
    description: str = None
    address: str = None
    business_phone_number: str = None
    currency: str

    class Config:
        from_attributes = True

