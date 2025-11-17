import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from db.session import Base

if TYPE_CHECKING:
    from .notes_db import Notes

class Users(Base):
    __tablename__ = "users_table"
    notes : Mapped[list["Notes"]] = relationship(back_populates="user", cascade="all, delete")

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name : Mapped[str] = mapped_column(String[50])
    last_name : Mapped[str] = mapped_column(String[50])
    email : Mapped[str] = mapped_column(String[100])
    age : Mapped[int] = mapped_column(Integer)
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())