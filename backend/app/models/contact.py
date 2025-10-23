from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Contact(Base):
    """
    Contact model for storing contact form submissions
    """
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    service_interest = Column(String(100), nullable=True)  # Optional field
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Status tracking
    is_read = Column(Boolean, default=False)
    is_responded = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    def __str__(self):
        return f"Contact from {self.name} ({self.email})"