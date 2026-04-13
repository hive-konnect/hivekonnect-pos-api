from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.core.database import init_db

# Create FastAPI instance
app = FastAPI(
    title="My API",
    description="Starter FastAPI application",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(auth_router)
# Health check endpoint (useful for deployments)
@app.get("/health")
def health_check():
    return {"status": "ok"}