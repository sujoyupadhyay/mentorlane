from fastapi import FastAPI
from app.v1.teaching_modes_api import router as teaching_modes_router
from app.v1.teaching_language_api import router as teaching_languages_router
from app.v1.teaching_levels_api import router as teaching_levels_router

# Create FastAPI app instance with enhanced configuration
app = FastAPI(
    title="MentorLane API",
    description="API for MentorLane database services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Include the teaching modes API router
app.include_router(teaching_modes_router)

# Include the teaching languages API router
app.include_router(teaching_languages_router)

# Include the teaching levels API router
app.include_router(teaching_levels_router)

# Define endpoints with proper documentation
@app.get(
    "/",
    summary="Root endpoint",
    description="Returns a welcome message",
    tags=["General"]
)
def read_root():
    """Welcome endpoint that returns a simple greeting message."""
    return {"message": "Hello MentorLane", "status": "active"}

@app.get(
    "/health",
    summary="Health check endpoint",
    description="Check the health status of the API",
    tags=["Health"]
)
def health_check():
    """Health check endpoint to verify API status."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2026-06-15T00:00:00Z"
    }
