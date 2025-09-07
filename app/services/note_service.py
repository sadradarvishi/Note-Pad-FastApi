from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.note_model import NoteModel
from app.models.user_model import UserModel
from app.schemas.note_schema import NoteCreate, NoteUpdate


class ConflictError(Exception): ...


def create_note(db: Session, payload: NoteCreate, current_user: UserModel):
    try:
        note = NoteModel(**payload.model_dump(), owner_id=current_user.id)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
    except Exception:
        db.rollback()
        raise


def update_note(db: Session, note: NoteModel, payload: NoteUpdate):
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(note, field, value)
    try:
        db.commit()
        db.refresh(note)
        return note
    except Exception:
        db.rollback()
        raise


def get_note_for_owner(db: Session, note_id: UUID, owner_id: UUID):
    stmt = select(NoteModel).where(NoteModel.id == note_id, NoteModel.owner_id == owner_id)
    return db.execute(stmt).scalars().one_or_none()


def get_all_notes_for_owner(db: Session, owner_id: UUID, offset: int = 0, limit: int = 10):
    stmt = (
        select(NoteModel)
        .where(NoteModel.owner_id == owner_id)
        .order_by(desc(NoteModel.created_at), desc(NoteModel.id))
        .offset(offset)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


def delete_note(db: Session, note: NoteModel):
    try:
        db.delete(note)
        db.commit()
        return None
    except Exception:
        db.rollback()
        raise
