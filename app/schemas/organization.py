from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    admin_email: EmailStr
    admin_password: str
    admin_name: str

class OrganizationResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    admin_user: dict  # Include admin user details in response
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True