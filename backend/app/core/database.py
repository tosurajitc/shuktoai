from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_db_connection():
    """
    Test database connection
    """
    try:
        # Try to create a connection and execute a simple query
        from sqlalchemy import text
        connection = engine.connect()
        result = connection.execute(text("SELECT 1"))
        connection.close()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def init_db():
    """
    Initialize database - create tables
    """
    try:
        # Import all models here (we'll create these later)
        from app.models import contact
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise