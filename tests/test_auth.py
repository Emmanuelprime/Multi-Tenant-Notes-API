import pytest

class TestAuthentication:
    """Test authentication endpoints."""
    
    @pytest.mark.asyncio
    async def test_login_success(self, client, test_organization):
        """Test successful login."""
        org_id = test_organization["id"]
        login_data = {
            "email": "admin@test.com",
            "password": "admin123"
        }
        
        response = await client.post(f"/auth/login/{org_id}", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == login_data["email"]
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, test_organization):
        """Test login with wrong password."""
        org_id = test_organization["id"]
        login_data = {
            "email": "admin@test.com",
            "password": "wrongpassword"
        }
        
        response = await client.post(f"/auth/login/{org_id}", json=login_data)
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client, test_organization):
        """Test login with non-existent user."""
        org_id = test_organization["id"]
        login_data = {
            "email": "nonexistent@test.com",
            "password": "password123"
        }
        
        response = await client.post(f"/auth/login/{org_id}", json=login_data)
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, client, admin_token):
        """Test getting current user info."""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.get("/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "role" in data
        assert data["role"] == "admin"
    
    @pytest.mark.asyncio
    async def test_get_current_user_with_org(self, client, admin_token):
        """Test getting current user info with organization."""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.get("/auth/me/with-org", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "organization" in data
        assert data["user"]["role"] == "admin"
    
    @pytest.mark.asyncio
    async def test_change_password(self, client, admin_token):
        """Test changing password."""
        headers = {"Authorization": f"Bearer {admin_token}"}
        change_data = {
            "current_password": "admin123",
            "new_password": "newadmin123"
        }
        
        response = await client.post("/auth/change-password", params=change_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Password updated successfully"
    
    @pytest.mark.asyncio
    async def test_change_password_wrong_current(self, client, admin_token):
        """Test changing password with wrong current password."""
        headers = {"Authorization": f"Bearer {admin_token}"}
        change_data = {
            "current_password": "wrongcurrent",
            "new_password": "newadmin123"
        }
        
        response = await client.post("/auth/change-password", params=change_data, headers=headers)
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_access_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token."""
        response = await client.get("/auth/me")
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_access_protected_endpoint_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/auth/me", headers=headers)
        assert response.status_code == 401