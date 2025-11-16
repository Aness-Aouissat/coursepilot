from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import notes_models
from app.dependencies import SessionDep
from app.db.models.notes_db import Notes

router = APIRouter(prefix = "/v1/notes")

@router.get("/")
async def get_all_notes(session: SessionDep, limit: int = 10) -> notes_models.NotesGet:
    result = await session.execute(select(Notes).order_by(Notes.created_at).limit(limit))
    notes = result.scalars().all()
    return notes_models.NotesGet.model_validate({"notes": notes})

@router.post("/")
async def create_note(session: SessionDep, note: notes_models.NoteCreate) -> notes_models.NoteResponse:
    note_orm = Notes(title = note.title, content = note.content)
    session.add(note_orm)
    await session.commit()
    await session.refresh(note_orm)
    return notes_models.NoteResponse.model_validate(note_orm)

@router.get("/{note_id}")
async def get_note(note_id: int) -> notes_models.NoteResponse:
    pass

@router.put("/{note_id}")
async def update_note(note_id: int, note: notes_models.NoteUpdate) -> notes_models.NoteResponse:
    pass

@router.delete("/{note_id}")
async def delete_note(note_id: int):
    pass