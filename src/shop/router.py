from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.auth.dependencies import CurrentOwner

from . import schemas, service
from src.core.database import get_db

router = APIRouter(prefix="/shops", tags=["Shops"])

@router.post("", response_model=schemas.ShopResponse)
def create_shop(shop: schemas.ShopCreate, current_user: CurrentOwner, db: Session = Depends(get_db)):
    return service.create_shop(
        db,
        owner_id=current_user.id,
        shop_name=shop.shop_name,
        shop_type=shop.shop_type,
        description=shop.description,
        address=shop.address,
        business_phone_number=shop.business_phone_number,
        currency=shop.currency,
    )


@router.get("/my", response_model=list[schemas.ShopResponse])
def get_my_shops(
    current_user: CurrentOwner,
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return service.list_owner_shops_paginated(db, owner_id=current_user.id, limit=limit, offset=offset)


@router.get("/{shop_id}", response_model=schemas.ShopResponse)
def get_shop(shop_id: UUID, current_user: CurrentOwner, db: Session = Depends(get_db)):
    shop = service.get_owner_shop(db, shop_id=shop_id, owner_id=current_user.id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop


@router.patch("/{shop_id}", response_model=schemas.ShopResponse)
def patch_shop(
    shop_id: UUID,
    payload: schemas.ShopUpdate,
    current_user: CurrentOwner,
    db: Session = Depends(get_db),
):
    shop = service.get_owner_shop(db, shop_id=shop_id, owner_id=current_user.id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return shop

    return service.update_owner_shop(db, shop=shop, updates=updates)
