import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base

if TYPE_CHECKING:
    from .courses_db import Courses
    from .notes_db import Notes

class Users(Base):
    __tablename__ = "users_table"
    notes: Mapped[list["Notes"]] = relationship(back_populates="user", cascade="all, delete")
    courses: Mapped[list["Courses"]] = relationship(back_populates="user", cascade="all, delete")

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String[50])
    first_name: Mapped[str] = mapped_column(String[50])
    last_name: Mapped[str] = mapped_column(String[50])
    email: Mapped[str] = mapped_column(String[125])
    hashed_password: Mapped[str] = mapped_column(String[255])
    age: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    disabled: Mapped[Boolean] = mapped_column(Boolean, default=False)