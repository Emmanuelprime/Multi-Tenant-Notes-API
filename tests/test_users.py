import pytest

class TestUsers:
    """Test user management endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_user_as_admin(self, client, test_organization, admin_token):
        """Test admin creating a new user."""
        org_id = test_organization["id"]
        user_data = {
            "email": "newuser@test.com",
            "password": "newuser123",
            "name": "New User",
            "role": "reader"
        }
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.post(
            f"/organizations/{org_id}/users/",
            json=user_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["role"] == user_data["role"]
        assert data["organization_id"] == org_id
    
    @pytest.mark.asyncio
    async def test_create_duplicate_user(self, client, test_organization, admin_token, test_user):
        """Test creating user with duplicate email in same organization."""
        org_id = test_organization["id"]
        user_data = {
            "email": "writer@test.com",  
            "password": "password123",
            "name": "Duplicate User",
            "role": "reader"
        }
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.post(
            f"/organizations/{org_id}/users/",
            json=user_data,
            headers=headers
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_create_user_unauthorized(self, client, test_organization, writer_token):
        """Test non-admin trying to create user."""
        org_id = test_organization["id"]
        user_data = {
            "email": "unauthorized@test.com",
            "password": "password123",
            "name": "Unauthorized User",
            "role": "reader"
        }
        
        headers = {"Authorization": f"Bearer {writer_token}"}
        response = await client.post(
            f"/organizations/{org_id}/users/",
            json=user_data,
            headers=headers
        )
        
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_list_users_as_admin(self, client, test_organization, admin_token, test_user):
        """Test admin listing organization users."""
        org_id = test_organization["id"]
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = await client.get(f"/organizations/{org_id}/users/", headers=headers)
        
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 2  # Admin + test writer user
    
    @pytest.mark.asyncio
    async def test_list_users_unauthorized(self, client, test_organization, writer_token):
        """Test non-admin trying to list users."""
        org_id = test_organization["id"]
        headers = {"Authorization": f"Bearer {writer_token}"}
        
        response = await client.get(f"/organizations/{org_id}/users/", headers=headers)
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_update_user_role(self, client, test_organization, admin_token, test_user):
        """Test admin updating user role."""
        org_id = test_organization["id"]
        user_id = test_user["id"]
        update_data = {"role": "admin"}
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(
            f"/organizations/{org_id}/users/{user_id}",
            json=update_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
    
    @pytest.mark.asyncio
    async def test_update_own_role(self, client, test_organization, admin_token):
        """Test admin trying to update their own role."""
        org_id = test_organization["id"]
        # Get admin user ID from organization
        org_response = await client.get(f"/organizations/{org_id}")
        admin_user_id = org_response.json()["admin_user"]["id"]
        
        update_data = {"role": "reader"}
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(
            f"/organizations/{org_id}/users/{admin_user_id}",
            json=update_data,
            headers=headers
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_delete_user(self, client, test_organization, admin_token):
        """Test admin deleting a user."""
        # First create a user to delete
        org_id = test_organization["id"]
        user_data = {
            "email": "todelete@test.com",
            "password": "password123",
            "name": "User To Delete",
            "role": "reader"
        }
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        create_response = await client.post(
            f"/organizations/{org_id}/users/",
            json=user_data,
            headers=headers
        )
        user_id = create_response.json()["id"]
        
        # Now delete the user
        delete_response = await client.delete(
            f"/organizations/{org_id}/users/{user_id}",
            headers=headers
        )
        
        assert delete_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_delete_own_account(self, client, test_organization, admin_token):
        """Test admin trying to delete their own account."""
        org_id = test_organization["id"]
        org_response = await client.get(f"/organizations/{org_id}")
        admin_user_id = org_response.json()["admin_user"]["id"]
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.delete(
            f"/organizations/{org_id}/users/{admin_user_id}",
            headers=headers
        )
        
        assert response.status_code == 400