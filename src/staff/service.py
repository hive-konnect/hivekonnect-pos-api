import secrets

from sqlalchemy.orm import Session
from uuid import UUID

from src.auth import utils as auth_utils
from src.shop.models import Shop

from .models import Staff


def _generate_pin(length: int = 6) -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def create_staff_member(
    db: Session,
    *,
    shop_id: UUID,
    display_name: str,
    role: str,
    phone: str | None = None,
) -> tuple[Staff, str]:
    pin = _generate_pin()
    staff = Staff(
        shop_id=shop_id,
        display_name=display_name,
        role=role,
        phone=phone,
        pin_hash=auth_utils.hash_password(pin),
        is_active=True,
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff, pin


def list_shop_staff(
    db: Session,
    *,
    shop_id: UUID,
    limit: int = 50,
    offset: int = 0,
    is_active: bool | None = None,
) -> list[Staff]:
    query = db.query(Staff).filter(Staff.shop_id == shop_id)
    if is_active is not None:
        query = query.filter(Staff.is_active.is_(is_active))
    return query.order_by(Staff.created_at.desc()).offset(offset).limit(limit).all()


def get_staff_member(db: Session, *, staff_id: UUID) -> Staff | None:
    return db.query(Staff).filter(Staff.id == staff_id).first()


def reset_staff_pin(db: Session, *, staff: Staff) -> tuple[Staff, str]:
    new_pin = _generate_pin()
    staff.pin_hash = auth_utils.hash_password(new_pin)
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff, new_pin


def disable_staff_member(db: Session, *, staff: Staff) -> Staff:
    staff.is_active = False
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def owner_controls_shop(db: Session, *, owner_id: UUID, shop_id: UUID) -> bool:
    return db.query(Shop).filter(Shop.id == shop_id, Shop.owner_id == owner_id).first() is not None
