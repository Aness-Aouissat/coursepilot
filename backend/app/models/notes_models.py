from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class NotesBase(BaseModel):
    title: str
    content: str | None = None 

class NoteCreate(NotesBase):
    pass

class NoteUpdate(BaseModel):
    title: str | None = None 
    content: str | None = None

class NoteRead(NotesBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class NoteList(BaseModel):
    notes: list[NoteRead]
