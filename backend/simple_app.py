from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple API for Testing")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "*",  # Allow all origins for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    message: str = Field(..., min_length=10)
    service_interest: Optional[str] = None


@app.post("/api/contact", status_code=201)
async def create_contact(contact: ContactCreate):
    """
    Create new contact form submission.
    """
    try:
        # Log the contact form submission for testing
        logger.info(f"Contact form submission: {contact}")
        
        # Return a successful response
        return {
            "id": 1,
            "name": contact.name,
            "email": contact.email,
            "message": contact.message,
            "service_interest": contact.service_interest,
            "status": "new"
        }
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Simple API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}