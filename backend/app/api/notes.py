from fastapi import APIRouter, Response, Query, Body, Path

from app.models.notes_models import NotesGet, NoteResponse, NoteCreate, NoteUpdate
from app.dependencies import SessionDep, UserDep
from app.services.notes_services import (
    get_all_notes_service,
    create_note_service, 
    get_note_service,
    update_note_service,
    delete_note_service
)

from typing import Annotated
import uuid

router = APIRouter(prefix = "/v1/notes")

@router.get("/", response_model=NotesGet)
async def get_all_notes(
    session: SessionDep, 
    user: UserDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    notes = await get_all_notes_service(user.id, limit, session)

    return {"notes": notes}

@router.post("/", response_model=NoteResponse)
async def create_note(
    session: SessionDep, 
    user: UserDep,
    note: Annotated[NoteCreate, Body()]
):
    note_orm = await create_note_service(user.id, note, session)

    return note_orm

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    session: SessionDep,
    user: UserDep, 
    note_id: Annotated[uuid.UUID, Path()]
):  
    note = await get_note_service(user.id, note_id, session)
    
    return note

@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(
    session: SessionDep, 
    user: UserDep,
    note_id: Annotated[uuid.UUID, Path()], 
    note: Annotated[NoteUpdate, Body()]
):
    updated_note = await update_note_service(user.id, note_id, note, session)
    
    return updated_note

@router.delete("/{note_id}")
async def delete_note(
    session: SessionDep, 
    user: UserDep,
    note_id: Annotated[uuid.UUID, Path()]
):
    await delete_note_service(user.id, note_id, session)
    return Response(status_code=204)