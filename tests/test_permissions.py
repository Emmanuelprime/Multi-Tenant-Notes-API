import pytest

class TestRolePermissions:
    """Test comprehensive role-based permissions."""
    
    @pytest.mark.asyncio
    async def test_reader_permissions(self, client, test_organization, admin_token):
        """Test all reader permissions."""
        # Create a reader user
        org_id = test_organization["id"]
        reader_data = {
            "email": "reader_user@test.com",
            "password": "reader123",
            "name": "Reader User",
            "role": "reader"
        }
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        user_response = await client.post(
            f"/organizations/{org_id}/users/",
            json=reader_data,
            headers=headers
        )
        
        # Login as reader
        login_response = await client.post(f"/auth/login/{org_id}", json={
            "email": "reader_user@test.com",
            "password": "reader123"
        })
        reader_token = login_response.json()["access_token"]
        reader_headers = {"Authorization": f"Bearer {reader_token}"}
        
        # Reader should be able to list notes
        list_response = await client.get("/notes/", headers=reader_headers)
        assert list_response.status_code == 200
        
        # Reader should NOT be able to create notes
        create_response = await client.post("/notes/", json={
            "title": "Test",
            "content": "Test"
        }, headers=reader_headers)
        assert create_response.status_code == 403
        
        # Reader should NOT be able to update notes
        update_response = await client.put("/notes/some_id", json={
            "title": "Updated"
        }, headers=reader_headers)
        assert update_response.status_code == 403
        
        # Reader should NOT be able to delete notes
        delete_response = await client.delete("/notes/some_id", headers=reader_headers)
        assert delete_response.status_code == 403
        
        # Reader should NOT be able to create users
        user_create_response = await client.post(
            f"/organizations/{org_id}/users/",
            json={
                "email": "new@test.com",
                "password": "pass",
                "name": "New",
                "role": "reader"
            },
            headers=reader_headers
        )
        assert user_create_response.status_code == 403
        
        # Reader should NOT be able to list users
        user_list_response = await client.get(
            f"/organizations/{org_id}/users/",
            headers=reader_headers
        )
        assert user_list_response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_writer_permissions(self, client, writer_token, test_organization):
        """Test all writer permissions."""
        org_id = test_organization["id"]
        writer_headers = {"Authorization": f"Bearer {writer_token}"}
        
        # Writer should be able to create notes
        create_response = await client.post("/notes/", json={
            "title": "Writer's Note",
            "content": "Content"
        }, headers=writer_headers)
        assert create_response.status_code == 200
        
        # Writer should be able to list notes
        list_response = await client.get("/notes/", headers=writer_headers)
        assert list_response.status_code == 200
        
        # Writer should NOT be able to create users
        user_create_response = await client.post(
            f"/organizations/{org_id}/users/",
            json={
                "email": "new@test.com",
                "password": "pass",
                "name": "New",
                "role": "reader"
            },
            headers=writer_headers
        )
        assert user_create_response.status_code == 403
        
        note_id = create_response.json()["id"]
        delete_response = await client.delete(f"/notes/{note_id}", headers=writer_headers)
        assert delete_response.status_code == 403