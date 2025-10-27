import pytest
import pytest_asyncio
import asyncio
import sys
import os
# Ensure workspace root is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))) )
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from main import app
from app.models.user import User
from app.models.organization import Organization
from app.models.note import Note
from app.services.auth import get_password_hash

# Test database configuration
TEST_MONGO_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "test_notes_api"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_database():
    """Setup test database and clean up after tests."""
    client = AsyncIOMotorClient(TEST_MONGO_URL)
    
    # Initialize Beanie with test database
    await init_beanie(
        database=client[TEST_DB_NAME],
        document_models=[User, Organization, Note]
    )
    
    yield
    
    # Clean up: drop test database after tests
    await client.drop_database(TEST_DB_NAME)
    client.close()

@pytest_asyncio.fixture
async def client(test_database):
    """Create a test client."""
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def test_organization(client):
    """Create a test organization and return its data."""
    org_data = {
        "name": "Test Organization",
        "description": "Test organization for pytest",
        "admin_email": "admin@test.com",
        "admin_password": "admin123",
        "admin_name": "Test Admin"
    }
    
    response = await client.post("/organizations/", json=org_data)
    assert response.status_code == 200
    org_response = response.json()
    
    return org_response

@pytest_asyncio.fixture
async def admin_token(client, test_organization):
    """Get admin JWT token for the test organization."""
    org_id = test_organization["id"]
    login_data = {
        "email": "admin@test.com",
        "password": "admin123"
    }
    
    response = await client.post(f"/auth/login/{org_id}", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    
    return token_data["access_token"]

@pytest_asyncio.fixture
async def test_user(client, test_organization, admin_token):
    """Create a test user and return user data."""
    org_id = test_organization["id"]
    user_data = {
        "email": "writer@test.com",
        "password": "writer123",
        "name": "Test Writer",
        "role": "writer"
    }
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.post(
        f"/organizations/{org_id}/users/",
        json=user_data,
        headers=headers
    )
    assert response.status_code == 200
    
    return response.json()

@pytest_asyncio.fixture
async def writer_token(client, test_organization, test_user):
    """Get writer JWT token."""
    org_id = test_organization["id"]
    login_data = {
        "email": "writer@test.com",
        "password": "writer123"
    }
    
    response = await client.post(f"/auth/login/{org_id}", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    
    return token_data["access_token"]