from fastapi import APIRouter, HTTPException, Response, Query
from sqlalchemy import select

from app.models import notes_models
from app.dependencies import SessionDep
from app.db.models.notes_db import Notes

from typing import Annotated
import uuid

router = APIRouter(prefix = "/v1/notes")

@router.get("/", response_model=notes_models.NotesGet)
async def get_all_notes(session: SessionDep, limit: Annotated[int, Query(ge=1, le=100)] = 10):
    result = await session.execute(select(Notes).order_by(Notes.created_at).limit(limit))
    notes = result.scalars().all()
    return {"notes": notes}

@router.post("/", response_model=notes_models.NoteResponse)
async def create_note(session: SessionDep, note: notes_models.NoteCreate):
    note_orm = Notes(title = note.title, content = note.content)
    session.add(note_orm)
    await session.commit()
    await session.refresh(note_orm)
    return note_orm

@router.get("/{note_id}", response_model=notes_models.NoteResponse)
async def get_note(session: SessionDep, note_id: uuid.UUID):
    result = await session.get(Notes, note_id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return result

@router.patch("/{note_id}", response_model=notes_models.NoteResponse)
async def update_note(session: SessionDep, note_id: uuid.UUID, note: notes_models.NoteUpdate):
    result = await session.get(Notes, note_id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    note_details = note.model_dump(exclude_unset=True)
    if not note_details:
        return result
    for key, value in note_details.items():
        if key in {'id', 'created_at', 'updated_at'}:
            continue
        setattr(result, key, value)
    await session.commit()
    await session.refresh(result)
    return result

@router.delete("/{note_id}")
async def delete_note(session: SessionDep, note_id: uuid.UUID):
    result = await session.get(Notes, note_id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    await session.delete(result)
    await session.commit()
    return Response(status_code=204)