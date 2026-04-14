from sqlalchemy.orm import Session


from . import models, utils


def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return None

    hashed = utils.hash_password(password)

    user = models.User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    if not utils.verify_password(password, user.hashed_password):
        return None

    return user

def authenticate_and_issue_token(db: Session, *, email: str, password: str) -> dict[str, str]:
    db_user = authenticate_user(db, email, password)
    if not db_user:
        raise ValueError("Invalid email or password")

    access_token = utils.create_token({"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}