from fastapi import APIRouter, Depends, HTTPException
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
    db_user = service.authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = utils.create_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def me(current_user=Depends(dependencies.get_current_user)):
    return current_user