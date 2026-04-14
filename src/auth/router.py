from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, service, utils, dependencies
from src.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = service.create_user(
            db,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if db_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user


@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return service.authenticate_and_issue_token(db, email=user.email, password=user.password)


@router.post("/token", response_model=schemas.TokenResponse)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return service.authenticate_and_issue_token(db, email=form_data.username, password=form_data.password)


@router.get("/me", response_model=schemas.UserResponse)
def me(current_user: dependencies.CurrentUser):
    return current_user