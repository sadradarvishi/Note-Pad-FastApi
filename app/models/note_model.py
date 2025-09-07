from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from app.database import Base

if TYPE_CHECKING:
    from app.models.user_model import UserModel


class NoteModel(Base):
    __tablename__: str = "notes_table"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid7, index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users_table.id"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(225), nullable=False, index=True)
    note_pad: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        index=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    owner: Mapped[UserModel] = relationship(
        "UserModel",
        back_populates="notes",
    )

    def __repr__(self):
        return f"<Notes(id='{self.id}' and title='{self.title}')>"
