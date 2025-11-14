from pydantic import BaseModel

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    
class NotesGet(BaseModel):
    notes: list[NoteResponse]

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None 
    content: str | None = None 
    
