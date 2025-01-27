from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from enum import Enum 

class ApplicationStatus(str, Enum):
    APPLIED ="Applied"
    INTERVEWED = "Intervewed"
    REJECTED ='Rejected'
    OFFERED ='Offered'

class Job(BaseModel):
    company: str  # This is the only required field
    application: Optional[str] = None
    contact_name: Optional[str] = None
    position: Optional[str] = None
    cover_letter: Optional[str] = None
    email: Optional[EmailStr] = None
    company_website: Optional[str] = None
    company_address: Optional[str] = None
    application_date: Optional[date] = None
    cover_letter_sent: Optional[bool] = None
    interview_date: Optional[date] = None
    how_did_you_find_them: Optional[str] = None
    resume: Optional[str] = None
    notes: Optional[str] = None
    application_status: Optional[ApplicationStatus] = None

