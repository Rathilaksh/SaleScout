"""
SaleScout Backend - FastAPI Application
Product price monitoring and alert system.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import FRONTEND_URL, DEBUG
from database import init_db
from routers.users import router as users_router
from routers.trackers import router as trackers_router
from routers.price_history import router as price_history_router

# Create FastAPI application
app = FastAPI(
    title="SaleScout API",
    description="Product price monitoring and alert system for Amazon & Flipkart",
    version="1.0.0",
    debug=DEBUG
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event handlers
@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()
    print("✅ Database initialized")


@app.on_event("shutdown")
def on_shutdown():
    """Cleanup on application shutdown."""
    print("👋 Shutting down SaleScout API")


# Include routers
app.include_router(users_router)
app.include_router(trackers_router)
app.include_router(price_history_router)


# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    API root endpoint - health check.
    """
    return {
        "message": "Welcome to SaleScout API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )
