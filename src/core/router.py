from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.core.database import engine


router = APIRouter(tags=["System"])


@router.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@router.get("/health", response_model=None)
def health_check() -> dict[str, str] | JSONResponse:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "degraded",
                "database": "disconnected",
                "error": str(exc.__class__.__name__),
            },
        )
