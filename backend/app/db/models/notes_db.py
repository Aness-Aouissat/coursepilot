import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base

if TYPE_CHECKING:
    from .users_db import Users

class Notes(Base):
    __tablename__ = "notes_table"
    user : Mapped["Users"] = relationship(back_populates="notes")
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"), nullable=False)

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title : Mapped[str] = mapped_column(String(255), nullable=True)
    content : Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())