from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.auth.router import router as auth_router
from src.core.config import settings
from src.core.database import engine, init_db

# Create FastAPI instance
app = FastAPI(
    title="My API",
    description="Starter FastAPI application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(auth_router, prefix=settings.API_V1_STR)
# Health check endpoint (useful for deployments)
@app.get("/health")
def health_check():
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