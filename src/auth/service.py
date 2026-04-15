from uuid import UUID

from sqlalchemy.orm import Session

from src.core.config import settings
from src.staff.models import Staff

from . import models, utils
from .exceptions import InvalidCredentials, UserAlreadyExists


def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> models.User:
    normalized_email = email.lower().strip()
    existing = db.query(models.User).filter(models.User.email == normalized_email).first()
    if existing:
        raise UserAlreadyExists()

    user = models.User(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=normalized_email,
        hashed_password=utils.hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    normalized_email = email.lower().strip()
    user = db.query(models.User).filter(models.User.email == normalized_email).first()
    if not user:
        return None
    if not utils.verify_password(password, user.hashed_password):
        return None
    return user


def authenticate_and_issue_owner_token(db: Session, *, email: str, password: str) -> dict[str, str | None]:
    db_user = authenticate_user(db, email, password)
    if not db_user:
        raise InvalidCredentials()

    token_payload = {
        "type": "owner",
        "user_id": db_user.id,
        "shop_id": None,
    }
    return {
        "access_token": utils.create_access_token(token_payload),
        "refresh_token": utils.create_refresh_token(token_payload),
        "token_type": "bearer",
    }


def issue_owner_access_from_refresh(db: Session, *, refresh_token: str) -> dict[str, str | None]:
    payload = utils.decode_token(refresh_token)
    if payload.get("token_use") != "refresh" or payload.get("type") != "owner":
        raise InvalidCredentials()

    user_id = payload.get("user_id")
    if not user_id:
        raise InvalidCredentials()

    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active.is_(True)).first()
    if not db_user:
        raise InvalidCredentials()

    access_token = utils.create_access_token(
        {
            "type": "owner",
            "user_id": db_user.id,
            "shop_id": None,
        }
    )
    return {"access_token": access_token, "refresh_token": None, "token_type": "bearer"}


def authenticate_staff_by_pin_and_issue_token(db: Session, *, shop_id: UUID, pin: str) -> dict[str, str | None]:
    staff_members = db.query(Staff).filter(Staff.is_active.is_(True), Staff.shop_id == shop_id).all()

    matching_staff = next((staff for staff in staff_members if utils.verify_password(pin, staff.pin_hash)), None)
    if not matching_staff:
        raise InvalidCredentials()

    access_token = utils.create_access_token(
        {
            "type": "staff",
            "staff_id": matching_staff.id,
            "shop_id": matching_staff.shop_id,
            "role": matching_staff.role,
        },
        expires_minutes=settings.STAFF_ACCESS_TOKEN_EXPIRE_HOURS * 60,
    )
    return {"access_token": access_token, "refresh_token": None, "token_type": "bearer"}
