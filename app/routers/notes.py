from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.services.note import NoteService
from app.services.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

def check_permission(user: User, action: str):
    """Check if user has permission for the requested action"""
    permissions = {
        "reader": ["read"],
        "writer": ["read", "create", "update"],
        "admin": ["read", "create", "update", "delete"]
    }
    
    if action not in permissions.get(user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with role '{user.role}' cannot perform '{action}' action"
        )

@router.post("/", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_active_user)
):
    check_permission(current_user, "create")
    
    note = await NoteService.create_note(
        note_data, 
        current_user.organization_id, 
        str(current_user.id)
    )
    
    return NoteResponse(
        id=str(note.id),
        title=note.title,
        content=note.content,
        organization_id=note.organization_id,
        created_by=note.created_by,
        created_at=note.created_at,
        updated_at=note.updated_at
    )

@router.get("/", response_model=List[NoteResponse])
async def list_notes(current_user: User = Depends(get_current_active_user)):
    check_permission(current_user, "read")
    
    notes = await NoteService.get_organization_notes(current_user.organization_id)
    return [
        NoteResponse(
            id=str(note.id),
            title=note.title,
            content=note.content,
            organization_id=note.organization_id,
            created_by=note.created_by,
            created_at=note.created_at,
            updated_at=note.updated_at
        ) for note in notes
    ]

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, current_user: User = Depends(get_current_active_user)):
    check_permission(current_user, "read")
    
    note = await NoteService.get_note(note_id, current_user.organization_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return NoteResponse(
        id=str(note.id),
        title=note.title,
        content=note.content,
        organization_id=note.organization_id,
        created_by=note.created_by,
        created_at=note.created_at,
        updated_at=note.updated_at
    )

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str, 
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_active_user)
):
    check_permission(current_user, "update")
    
    note = await NoteService.get_note(note_id, current_user.organization_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if current_user.role in ["writer"] and note.created_by != str(current_user.id):
        raise HTTPException(
            status_code=403, 
            detail="Can only update your own notes"
        )
    
    updated_note = await NoteService.update_note(
        note_id, note_data, current_user.organization_id
    )
    
    return NoteResponse(
        id=str(updated_note.id),
        title=updated_note.title,
        content=updated_note.content,
        organization_id=updated_note.organization_id,
        created_by=updated_note.created_by,
        created_at=updated_note.created_at,
        updated_at=updated_note.updated_at
    )

@router.delete("/{note_id}")
async def delete_note(note_id: str, current_user: User = Depends(get_current_active_user)):
    check_permission(current_user, "delete")
    
    note = await NoteService.get_note(note_id, current_user.organization_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if current_user.role == "writer" and note.created_by != str(current_user.id):
        raise HTTPException(
            status_code=403, 
            detail="Can only delete your own notes"
        )
    
    success = await NoteService.delete_note(note_id, current_user.organization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"message": "Note deleted successfully"}