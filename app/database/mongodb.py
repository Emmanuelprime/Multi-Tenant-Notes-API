import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.models.organization import Organization
from app.models.note import Note

client = None

async def connect_to_mongo():
    global client
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    database_name = os.getenv("MONGO_DB", "notes_api")
    
    client = AsyncIOMotorClient(mongo_url)
    await init_beanie(
        database=client[database_name],
        document_models=[User, Organization, Note]
    )

async def close_mongo_connection():
    if client:
        client.close()