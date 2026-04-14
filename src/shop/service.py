from .models import Shop
from sqlalchemy.orm import Session


def create_shop(db: Session, owner_id: str, shop_name: str, shop_type: str = "General", description: str = None, address: str = None, business_phone_number: str = None):
    shop = Shop(
        shop_name=shop_name,
        shop_type=shop_type,
        description=description,
        address=address,
        business_phone_number=business_phone_number,
        owner_id=owner_id
    )
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop