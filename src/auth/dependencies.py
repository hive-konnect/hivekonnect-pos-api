from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_db
from src.core.errors import UnauthorizedError
from src.staff.models import Staff

from .models import User
from .utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_token(token)
    except InvalidTokenError as exc:
        raise UnauthorizedError("Invalid token") from exc

    if payload.get("token_use") != "access":
        raise UnauthorizedError("Access token required")

    return payload


def get_current_owner(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> User:
    if payload.get("type") != "owner":
        raise UnauthorizedError("Owner token required")

    user_id = payload.get("user_id")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    user = db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first()
    if user is None:
        raise UnauthorizedError("User not found or disabled")
    return user


def get_current_staff(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> Staff:
    if payload.get("type") != "staff":
        raise UnauthorizedError("Staff token required")

    staff_id = payload.get("staff_id")
    if not staff_id:
        raise UnauthorizedError("Invalid token payload")

    staff = db.query(Staff).filter(Staff.id == staff_id, Staff.is_active.is_(True)).first()
    if staff is None:
        raise UnauthorizedError("Staff not found or disabled")
    return staff


CurrentOwner = Annotated[User, Depends(get_current_owner)]
CurrentStaff = Annotated[Staff, Depends(get_current_staff)]
CurrentUser = CurrentOwner
