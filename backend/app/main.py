from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .api.routes import contact_routes
from .core.config import settings
from app.core.database import init_db, test_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Services Platform API",
    description="Backend API for AI Services Platform - Healthcare Analytics & AI Solutions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact_routes.router, prefix="/api", tags=["contact"])



@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to the AI Services Platform API",
        "version": "0.1.0",
        "project": settings.PROJECT_NAME,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = test_db_connection()
    
    return {
        "status": "healthy" if db_status else "degraded",
        "service": "AI Services Platform API",
        "database": "connected" if db_status else "disconnected",
        "version": "0.1.0"
    }

@app.get("/api/db-status")
async def database_status():
    """Check database connection status"""
    try:
        db_connected = test_db_connection()
        return {
            "database_connected": db_connected,
            "database_url": f"postgresql://{settings.DB_USER}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
            "status": "success" if db_connected else "failed"
        }
    except Exception as e:
        logger.error(f"Database status check failed: {e}")
        return {
            "database_connected": False,
            "error": str(e),
            "status": "error"
        }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 AI Services Platform API starting up...")
    
    # Test database connection
    logger.info("Testing database connection...")
    if test_db_connection():
        logger.info("✅ Database connection successful")
        logger.info("Database initialization ready (models pending)")
    else:
        logger.error("❌ Database connection failed")
    
    logger.info(f"📊 Project: {settings.PROJECT_NAME}")
    logger.info(f"🗄️  Database: {settings.DB_NAME}")
    logger.info(f"🌐 Server: {settings.SERVER_HOST}")
    logger.info("🎉 AI Services Platform API startup complete!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 AI Services Platform API shutting down...")