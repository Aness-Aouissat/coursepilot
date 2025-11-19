from fastapi import APIRouter, HTTPException, Response, Query, Body, Path, Depends
from sqlalchemy import select

from app.models import notes_models
from app.dependencies import SessionDep, oauth2_scheme
from app.db.models.notes_db import Notes

from typing import Annotated
import uuid

router = APIRouter(prefix = "/v1/notes")

@router.get("/", response_model=notes_models.NotesGet)
async def get_all_notes(
    session: SessionDep, 
    token: Annotated[str, Depends(oauth2_scheme)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    result = await session.execute(select(Notes).order_by(Notes.created_at).limit(limit))
    notes = result.scalars().all()

    return {"notes": notes}

@router.post("/", response_model=notes_models.NoteResponse)
async def create_note(
    session: SessionDep, 
    token: Annotated[str, Depends(oauth2_scheme)],
    note: Annotated[notes_models.NoteCreate, Body()]
):
    note_orm = Notes(title = note.title, content = note.content)
    session.add(note_orm)

    await session.commit()
    await session.refresh(note_orm)
    return note_orm

@router.get("/{note_id}", response_model=notes_models.NoteResponse)
async def get_note(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)], 
    note_id: Annotated[uuid.UUID, Path()]
):
    result = await session.get(Notes, note_id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return result

@router.patch("/{note_id}", response_model=notes_models.NoteResponse)
async def update_note(
    session: SessionDep, 
    token: Annotated[str, Depends(oauth2_scheme)],
    note_id: Annotated[uuid.UUID, Path()], 
    note: Annotated[notes_models.NoteUpdate, Body()]
):
    result = await session.get(Notes, note_id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note_details = note.model_dump(exclude_unset=True)
    if not note_details:
        return result
    
    protected = {'id', 'user_id', 'created_at', 'updated_at'}
    [setattr(result, key, value) for key, value in note_details.items() if key not in protected]
    
    await session.commit()
    await session.refresh(result)
    return result

@router.delete("/{note_id}")
async def delete_note(
    session: SessionDep, 
    token: Annotated[str, Depends(oauth2_scheme)],
    note_id: Annotated[uuid.UUID, Path()]
):
    result = await session.get(Notes, note_id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await session.delete(result)
    await session.commit()
    return Response(status_code=204)