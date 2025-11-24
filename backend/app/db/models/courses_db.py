import uuid
from typing import TYPE_CHECKING 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base

if TYPE_CHECKING:
    from .users_db import Users
    from .notes_db import Notes

class Courses(Base):
    __tablename__ = "courses_table"
    user: Mapped["Users"] = relationship(back_populates="courses")
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"), nullable=False)
    notes: Mapped["Notes"] = relationship(back_populates="course")

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())