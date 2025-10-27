from typing import Optional
from beanie import Document
from pydantic import Field
from datetime import datetime

class Note(Document):
    title: str
    content: str
    organization_id: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "notes"
        indexes = [
            [("organization_id", 1)],  # This is For tenant isolation
        ]
        
    class Config:
        schema_extra = {
            "example": {
                "title": "My First Note",
                "content": "This is the content of my note",
                "organization_id": "org_123",
                "created_by": "user_123"
            }
        }