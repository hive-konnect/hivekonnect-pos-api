from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import settings

# Shared SQLAlchemy base for all models.
Base = declarative_base()

engine_kwargs = {"pool_pre_ping": True}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    # Imports ensure models are registered before table creation.
    from src.auth import models  # noqa: F401
    from src.shop import models  # noqa: F401
    from src.staff import models  # noqa: F401

    if settings.ENVIRONMENT.lower() in {"prod", "production"}:
        # In production use Alembic migrations, never implicit create_all.
        return

    Base.metadata.create_all(bind=engine)
