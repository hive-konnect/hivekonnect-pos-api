from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI(
    title="My API",
    description="Starter FastAPI application",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Health check endpoint (useful for deployments)
@app.get("/health")
def health_check():
    return {"status": "ok"}