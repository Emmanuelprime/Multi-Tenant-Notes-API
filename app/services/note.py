from typing import List
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from bson import ObjectId

class NoteService:
    @staticmethod
    async def create_note(note_data: NoteCreate, organization_id: str, user_id: str):
        note_dict = note_data.dict()
        note_dict["organization_id"] = organization_id
        note_dict["created_by"] = user_id
        
        note = Note(**note_dict)
        return await note.insert()
    
    @staticmethod
    async def get_note(note_id: str, organization_id: str):
        
        try:
            obj_id = ObjectId(note_id)
        except Exception:
            return None
        return await Note.find_one({"_id": obj_id, "organization_id": organization_id})
    
    @staticmethod
    async def get_organization_notes(organization_id: str) -> List[Note]:
        return await Note.find({"organization_id": organization_id}).to_list()
    
    @staticmethod
    async def update_note(note_id: str, note_data: NoteUpdate, organization_id: str):
        
        try:
            obj_id = ObjectId(note_id)
        except Exception:
            return None
        note = await Note.find_one({"_id": obj_id, "organization_id": organization_id})
        if note:
            update_data = note_data.dict(exclude_unset=True)
            await note.set(update_data)
            return note
        return None
    
    @staticmethod
    async def delete_note(note_id: str, organization_id: str):
        
        try:
            obj_id = ObjectId(note_id)
        except Exception:
            return False
        note = await Note.find_one({"_id": obj_id, "organization_id": organization_id})
        if note:
            await note.delete()
            return True
        return False