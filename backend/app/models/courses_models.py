from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class CoursesBase(BaseModel):
    title: str
    description: str | None = None

class CourseCreate(CoursesBase):
    pass

class CourseUpdate(BaseModel):
    title: str | None = None 
    description: str | None = None 

class CourseRead(CoursesBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class CourseList(BaseModel):
    courses: list[CourseRead]
