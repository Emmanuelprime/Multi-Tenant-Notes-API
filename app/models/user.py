from typing import Optional
from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime

class User(Document):
    email: EmailStr
    password: str
    name: str
    role: str = Field(..., description="User role: reader, writer, or admin")
    organization_id: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            [("organization_id", 1), ("email", 1)], 
        ]
        
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "Emmanuel Prime",
                "role": "writer",
                "organization_id": "org_123"
            }
        }