import pytest

class TestNotes:
    """Test notes endpoints with role-based access control."""
    
    @pytest.mark.asyncio
    async def test_create_note_as_writer(self, client, writer_token):
        """Test writer creating a note."""
        note_data = {
            "title": "Test Note from Writer",
            "content": "This is a test note created by a writer"
        }
        
        headers = {"Authorization": f"Bearer {writer_token}"}
        response = await client.post("/notes/", json=note_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == note_data["title"]
        assert data["content"] == note_data["content"]
        return data  # Return for use in other tests
    
    @pytest.mark.asyncio
    async def test_create_note_as_reader(self, client, test_organization, admin_token):
        """Test reader trying to create a note (should fail)."""
        # First create a reader user
        org_id = test_organization["id"]
        reader_data = {
            "email": "reader@test.com",
            "password": "reader123",
            "name": "Test Reader",
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
            "email": "reader@test.com",
            "password": "reader123"
        })
        reader_token = login_response.json()["access_token"]
        
        # Try to create note as reader
        note_data = {
            "title": "Test Note from Reader",
            "content": "This should fail"
        }
        
        reader_headers = {"Authorization": f"Bearer {reader_token}"}
        response = await client.post("/notes/", json=note_data, headers=reader_headers)
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_list_notes(self, client, writer_token):
        """Test listing notes."""
        headers = {"Authorization": f"Bearer {writer_token}"}
        response = await client.get("/notes/", headers=headers)
        
        assert response.status_code == 200
        notes = response.json()
        assert isinstance(notes, list)
    
    @pytest.mark.asyncio
    async def test_get_note(self, client, writer_token):
        """Test getting a specific note."""
        # First create a note
        note_data = {
            "title": "Note to Retrieve",
            "content": "This note will be retrieved"
        }
        
        headers = {"Authorization": f"Bearer {writer_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=headers)
        note_id = create_response.json()["id"]
        
        # Now retrieve it
        get_response = await client.get(f"/notes/{note_id}", headers=headers)
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == note_id
        assert data["title"] == note_data["title"]
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_note(self, client, writer_token):
        """Test getting a note that doesn't exist."""
        headers = {"Authorization": f"Bearer {writer_token}"}
        response = await client.get("/notes/nonexistent_id", headers=headers)
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_note_as_owner(self, client, writer_token):
        """Test writer updating their own note."""
        # First create a note
        note_data = {
            "title": "Note to Update",
            "content": "Original content"
        }
        
        headers = {"Authorization": f"Bearer {writer_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=headers)
        note_id = create_response.json()["id"]
        
        # Update the note
        update_data = {
            "title": "Updated Note Title",
            "content": "Updated content"
        }
        
        update_response = await client.put(
            f"/notes/{note_id}",
            json=update_data,
            headers=headers
        )
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
    
    @pytest.mark.asyncio
    async def test_update_others_note_as_writer(self, client, test_organization, admin_token, writer_token):
        """Test writer trying to update another user's note (should fail)."""
        # First create a note as admin
        note_data = {
            "title": "Admin's Note",
            "content": "This note belongs to admin"
        }
        
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=admin_headers)
        note_id = create_response.json()["id"]
        
        # Try to update as writer
        update_data = {"title": "Unauthorized Update"}
        writer_headers = {"Authorization": f"Bearer {writer_token}"}
        update_response = await client.put(
            f"/notes/{note_id}",
            json=update_data,
            headers=writer_headers
        )
        
        assert update_response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_update_note_as_admin(self, client, admin_token, writer_token):
        """Test admin updating another user's note."""
        # First create a note as writer
        note_data = {
            "title": "Writer's Note",
            "content": "This note belongs to writer"
        }
        
        writer_headers = {"Authorization": f"Bearer {writer_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=writer_headers)
        note_id = create_response.json()["id"]
        
        # Update as admin
        update_data = {"title": "Updated by Admin"}
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        update_response = await client.put(
            f"/notes/{note_id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert update_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_delete_note_as_admin(self, client, admin_token, writer_token):
        """Test admin deleting another user's note."""
        # First create a note as writer
        note_data = {
            "title": "Note to Delete",
            "content": "This note will be deleted by admin"
        }
        
        writer_headers = {"Authorization": f"Bearer {writer_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=writer_headers)
        note_id = create_response.json()["id"]
        
        # Delete as admin
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        delete_response = await client.delete(f"/notes/{note_id}", headers=admin_headers)
        
        assert delete_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_delete_own_note_as_writer(self, client, writer_token):
        """Test writer trying to delete their own note (should fail - writers can't delete)."""
        # First create a note
        note_data = {
            "title": "Writer's Note to Delete",
            "content": "This note can't be deleted by writer"
        }
        
        headers = {"Authorization": f"Bearer {writer_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=headers)
        note_id = create_response.json()["id"]
        
        # Try to delete as writer
        delete_response = await client.delete(f"/notes/{note_id}", headers=headers)
        assert delete_response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_tenant_isolation(self, client, test_organization, admin_token):
        """Test that notes are isolated between organizations."""
        # Create a second organization
        org2_data = {
            "name": "Second Organization",
            "description": "Second test organization",
            "admin_email": "admin2@test.com",
            "admin_password": "admin2123",
            "admin_name": "Second Admin"
        }
        
        org2_response = await client.post("/organizations/", json=org2_data)
        org2_id = org2_response.json()["id"]
        
        # Login as admin of second organization
        login_response = await client.post(f"/auth/login/{org2_id}", json={
            "email": "admin2@test.com",
            "password": "admin2123"
        })
        org2_token = login_response.json()["access_token"]
        
        # Create note in second organization
        note_data = {
            "title": "Note in Second Org",
            "content": "This note is in the second organization"
        }
        
        org2_headers = {"Authorization": f"Bearer {org2_token}"}
        create_response = await client.post("/notes/", json=note_data, headers=org2_headers)
        org2_note_id = create_response.json()["id"]
        
        # Try to access note from first organization (should fail)
        org1_headers = {"Authorization": f"Bearer {admin_token}"}
        get_response = await client.get(f"/notes/{org2_note_id}", headers=org1_headers)
        assert get_response.status_code == 404