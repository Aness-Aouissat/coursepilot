from pydantic import BaseModel, ConfigDict
import uuid

class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    title: str
    content: str
    
class NotesGet(BaseModel):
    notes: list[NoteResponse]

class NoteCreate(BaseModel):
    title: str 
    content: str | None = None

class NoteUpdate(BaseModel):
    title: str | None = None 
    content: str | None = None 
    
