from fastapi import APIRouter
from models import notes_models

router = APIRouter(prefix = "/v1/notes")

@router.get("/")
async def get_notes() -> notes_models.NotesGet:
    pass

@router.post("/")
async def create_note(note: notes_models.NoteCreate) -> notes_models.NoteResponse:
    pass

@router.get("/{note_id}")
async def get_note(note_id: int) -> notes_models.NoteResponse:
    pass

@router.put("/{note_id}")
async def update_note(note_id: int, note: notes_models.NoteUpdate) -> notes_models.NoteResponse:
    pass

@router.delete("/{note_id}")
async def delete_note(note_id: int):
    pass