from fastapi import APIRouter

from src.auth.router import router as auth_router

from src.shop.router import router as shop_router
api_router = APIRouter()

# Register feature routers here as the app grows.
api_router.include_router(auth_router)
api_router.include_router(shop_router)


