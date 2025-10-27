import pytest

class TestOrganizations:
    """Test organization endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_organization(self, client):
        """Test creating a new organization."""
        org_data = {
            "name": "New Test Org",
            "description": "A new test organization",
            "admin_email": "newadmin@test.com",
            "admin_password": "newadmin123",
            "admin_name": "New Admin"
        }
        
        response = await client.post("/organizations/", json=org_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == org_data["name"]
        assert data["description"] == org_data["description"]
        assert "admin_user" in data
        assert data["admin_user"]["email"] == org_data["admin_email"]
        assert data["admin_user"]["role"] == "admin"
    
    @pytest.mark.asyncio
    async def test_create_organization_duplicate_admin_email(self, client):
        """Test creating organization with duplicate admin email."""
        org_data = {
            "name": "Another Org",
            "description": "Another test organization",
            "admin_email": "admin@test.com",  # Same email as existing org
            "admin_password": "password123",
            "admin_name": "Another Admin"
        }
        
        response = await client.post("/organizations/", json=org_data)
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_get_organization(self, client, test_organization):
        """Test getting organization details."""
        org_id = test_organization["id"]
        response = await client.get(f"/organizations/{org_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == org_id
        assert data["name"] == test_organization["name"]
        assert "admin_user" in data
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_organization(self, client):
        """Test getting a organization that doesn't exist."""
        response = await client.get("/organizations/nonexistent_id")
        assert response.status_code == 404