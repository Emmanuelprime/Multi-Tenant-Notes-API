from typing import Optional
from beanie import Document
from pydantic import Field
from datetime import datetime

class Organization(Document):
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(None, description="Organization description")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "organizations"
        
    class Config:
        schema_extra = {
            "example": {
                "name": "Prime Robotics",
                "description": "A sample organization"
            }
        }