from fastapi import APIRouter

from src.auth.router import router as auth_router


api_router = APIRouter()

# Register feature routers here as the app grows.
api_router.include_router(auth_router)
