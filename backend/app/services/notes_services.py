from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.notes_db import Notes
from app.db.models.courses_db import Courses
from app.models.notes_models import NoteCreate, NoteUpdate

import uuid

async def get_all_notes_service(
    user_id: uuid.UUID, 
    course_id: uuid.UUID, 
    limit: int, 
    session: AsyncSession
):
    result = await session.execute(
        select(Notes)
        .join(Notes.course)
        .where(Notes.course_id == course_id)
        .where(Courses.user_id == user_id)
        .order_by(Notes.created_at)
        .limit(limit)
)
    notes = result.scalars().all()
    
    return notes

async def create_note_service( 
    course_id: uuid.UUID,
    data: NoteCreate,
    session: AsyncSession
):
    note = Notes(course_id = course_id, title = data.title, content = data.content)

    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note

async def get_note_service(
    user_id: uuid.UUID,
    note_id: uuid.UUID,
    session: AsyncSession
):
    note = await session.get(Notes, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.course.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    return note

async def update_note_service(
    user_id: uuid.UUID,
    note_id: uuid.UUID,
    data: NoteUpdate,
    session: AsyncSession
):
    note = await session.get(Notes, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.course.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    note_update_details = data.model_dump(exclude_unset=True)
    if not note_update_details:
        return note
    
    protected = {'id', 'user_id', 'created_at', 'updated_at'}
    [setattr(note, key, value) for key, value in note_update_details.items() if key not in protected]

    await session.commit()
    await session.refresh(note)
    return note

async def delete_note_service(
    user_id: uuid.UUID, 
    note_id: uuid.UUID,
    session: AsyncSession
):
    note = await session.get(Notes, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.course.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    await session.delete(note)
    await session.commit()