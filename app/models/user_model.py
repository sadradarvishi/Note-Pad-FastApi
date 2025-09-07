from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from app.database import Base

if TYPE_CHECKING:
    from app.models.note_model import NoteModel


class UserModel(Base):
    __tablename__: str = "users_table"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid7, index=True
    )
    firstname: Mapped[str] = mapped_column(
        String(225),
        nullable=False,
    )
    lastname: Mapped[str] = mapped_column(String(225), nullable=False)
    username: Mapped[str] = mapped_column(String(225), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(225), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    notes: Mapped[list[NoteModel]] = relationship(
        "NoteModel",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Users(id='{self.id}' and username='{self.username}')>"
