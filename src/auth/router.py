from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.database import get_db

from . import dependencies, schemas, service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(
        db,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
    )


@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return service.authenticate_and_issue_owner_token(db, email=user.email, password=user.password)


@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(payload: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    return service.issue_owner_access_from_refresh(db, refresh_token=payload.refresh_token)


@router.post("/pin-login", response_model=schemas.TokenResponse)
def pin_login(payload: schemas.PinLoginRequest, db: Session = Depends(get_db)):
    return service.authenticate_staff_by_pin_and_issue_token(db, shop_id=payload.shop_id, pin=payload.pin)


@router.post("/logout", response_model=schemas.LogoutResponse)
def logout(_: dict = Depends(dependencies.get_token_payload)):
    return {"message": "Logged out"}


@router.get("/me", response_model=schemas.UserResponse)
def me(current_user: dependencies.CurrentUser):
    return current_user
