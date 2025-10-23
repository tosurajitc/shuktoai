import logging
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
# Import all models here to ensure they're registered with SQLAlchemy
from app.models.contact import Contact
# Import any other models here

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize the database by creating all tables."""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise