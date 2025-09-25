from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from app.config import settings
from app.database import engine, Base
from app.routers import articles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"{request.method} {request.url.path} - Client: {request.client.host}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - Time: {process_time:.4f}s")
    
    return response


# Include routers
app.include_router(articles.router)


# Root endpoint
@app.get("/", response_model=dict)
def root():
    """Root endpoint with API information"""
    return {
        "success": True,
        "message": "Blog Platform API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "articles": {
                "POST /api/articles": "Create article",
                "GET /api/articles": "Get all articles",
                "GET /api/articles/{slug}": "Get article by slug",
                "PUT /api/articles/{slug}": "Update article",
                "DELETE /api/articles/{slug}": "Delete article"
            }
        }
    }


# Health check endpoint
@app.get("/health", response_model=dict)
def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "Service is healthy",
        "timestamp": time.time()
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if settings.debug else "Something went wrong"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
