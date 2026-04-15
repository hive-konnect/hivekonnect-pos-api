from .models import Shop
from sqlalchemy.orm import Session
from uuid import UUID


def create_shop(
    db: Session,
    owner_id: UUID,
    shop_name: str,
    shop_type: str = "General",
    description: str | None = None,
    address: str | None = None,
    business_phone_number: str | None = None,
    currency: str = "UGX",
):
    shop = Shop(
        shop_name=shop_name,
        shop_type=shop_type,
        description=description,
        address=address,
        business_phone_number=business_phone_number,
        currency=currency,
        owner_id=owner_id,
    )
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop


def list_owner_shops(db: Session, owner_id: UUID) -> list[Shop]:
    return db.query(Shop).filter(Shop.owner_id == owner_id).order_by(Shop.created_at.desc()).all()


def list_owner_shops_paginated(db: Session, owner_id: UUID, *, limit: int, offset: int) -> list[Shop]:
    return (
        db.query(Shop)
        .filter(Shop.owner_id == owner_id)
        .order_by(Shop.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_owner_shop(db: Session, shop_id: UUID, owner_id: UUID) -> Shop | None:
    return db.query(Shop).filter(Shop.id == shop_id, Shop.owner_id == owner_id).first()


def update_owner_shop(db: Session, shop: Shop, updates: dict) -> Shop:
    for key, value in updates.items():
        setattr(shop, key, value)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop
