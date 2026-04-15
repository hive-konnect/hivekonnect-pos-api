from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
import jwt
from jwt import InvalidTokenError

from src.core.config import settings

BCRYPT_MAX_PASSWORD_BYTES = 72


def _normalize_jwt_payload(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dict):
        return {k: _normalize_jwt_payload(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_jwt_payload(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_normalize_jwt_payload(v) for v in value)
    return value


def _password_byte_length(password: str) -> int:
    return len(password.encode("utf-8"))


def hash_password(password: str) -> str:
    if _password_byte_length(password) > BCRYPT_MAX_PASSWORD_BYTES:
        raise ValueError("Password is too long. Please use 72 bytes or fewer.")
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if _password_byte_length(plain) > BCRYPT_MAX_PASSWORD_BYTES:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def _create_token(data: dict, expires_delta: timedelta, token_use: str) -> str:
    to_encode = _normalize_jwt_payload(data.copy())
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    to_encode["token_use"] = token_use
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    ttl_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    return _create_token(data=data, expires_delta=timedelta(minutes=ttl_minutes), token_use="access")


def create_refresh_token(data: dict, expires_days: int | None = None) -> str:
    ttl_days = expires_days or settings.REFRESH_TOKEN_EXPIRE_DAYS
    return _create_token(data=data, expires_delta=timedelta(days=ttl_days), token_use="refresh")


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
    except InvalidTokenError:
        raise
