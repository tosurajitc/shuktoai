from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...models.contact import Contact
from ...schemas.contact_schemas import (
    ContactCreate, 
    ContactResponse, 
    ContactSuccessResponse,
    ContactUpdate,
    ContactListResponse
)

# Optional: Import email service if you want to send notifications
# from app.services.email import send_contact_notification

router = APIRouter()


@router.post("/contact", response_model=ContactSuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new contact from contact form submission
    This is the endpoint your ContactForm.js connects to
    """
    try:
        # Create new contact instance
        new_contact = Contact(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message,
            service_interest=contact_data.service_interest
        )
        
        # Save to database
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        
        # Optional: Send email notification to admin
        # try:
        #     await send_contact_notification(contact_data)
        # except Exception as e:
        #     # Log email error but don't fail the contact creation
        #     print(f"Email notification failed: {e}")
        
        return ContactSuccessResponse(
            success=True,
            message="Thank you for your message! We'll get back to you within 24 hours.",
            contact_id=new_contact.id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit contact form. Please try again."
        )


@router.get("/contacts", response_model=ContactListResponse)
async def get_contacts(
    page: int = 1,
    per_page: int = 20,
    unread_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all contacts (admin endpoint)
    """
    offset = (page - 1) * per_page
    
    query = db.query(Contact)
    
    if unread_only:
        query = query.filter(Contact.is_read == False)
    
    total = query.count()
    contacts = query.order_by(Contact.created_at.desc()).offset(offset).limit(per_page).all()
    
    return ContactListResponse(
        contacts=contacts,
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Get a specific contact by ID
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact_status(
    contact_id: int,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db)
):
    """
    Update contact status (mark as read/responded)
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Update fields if provided
    if contact_update.is_read is not None:
        contact.is_read = contact_update.is_read
    if contact_update.is_responded is not None:
        contact.is_responded = contact_update.is_responded
    
    db.commit()
    db.refresh(contact)
    
    return contact


@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Delete a contact (admin only)
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    
    return {"message": "Contact deleted successfully"}


# Health check for contact API
@router.get("/contact/health")
async def contact_health_check():
    """
    Health check for contact API
    """
    return {"status": "healthy", "service": "contact_api"}