from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth.dependencies import CurrentUser

from . import schemas, service
from src.core.database import get_db

router = APIRouter(prefix="/shops", tags=["Shops"])

@router.post("/", response_model=schemas.ShopResponse)
def create_shop(shop: schemas.ShopCreate, current_user: CurrentUser ,db: Session = Depends(get_db)):
    try:

        db_shop = service.create_shop(
            db,
            owner_id=current_user.id,
            shop_name=shop.shop_name,
            shop_type=shop.shop_type,
            description=shop.description,
            address=shop.address,
            business_phone_number=shop.business_phone_number
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return db_shop