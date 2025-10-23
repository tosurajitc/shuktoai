from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class ContactCreate(BaseModel):
    """
    Schema for creating a new contact (incoming data from frontend)
    """
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    message: str = Field(..., min_length=10, max_length=2000, description="Contact message")
    service_interest: Optional[str] = Field(None, max_length=100, description="Service of interest")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "message": "I'm interested in your AI development services for my healthcare startup.",
                "service_interest": "ai-development"
            }
        }


class ContactResponse(BaseModel):
    """
    Schema for contact response (what we send back to frontend)
    """
    id: int
    name: str
    email: str
    message: str
    service_interest: Optional[str]
    created_at: datetime
    is_read: bool
    is_responded: bool
    
    class Config:
        from_attributes = True  # For SQLAlchemy model conversion


class ContactUpdate(BaseModel):
    """
    Schema for updating contact status (admin use)
    """
    is_read: Optional[bool] = None
    is_responded: Optional[bool] = None


class ContactListResponse(BaseModel):
    """
    Schema for listing contacts with pagination info
    """
    contacts: list[ContactResponse]
    total: int
    page: int
    per_page: int
    
    
class ContactSuccessResponse(BaseModel):
    """
    Schema for successful contact form submission
    """
    success: bool = True
    message: str = "Thank you for your message! We'll get back to you within 24 hours."
    contact_id: int