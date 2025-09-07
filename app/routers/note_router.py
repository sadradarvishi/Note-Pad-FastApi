from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependency.auth import get_current_user
from app.models.user_model import UserModel
from app.schemas import note_schema
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[note_schema.NoteRead], status_code=status.HTTP_200_OK)
def list_all_notes(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        return note_service.get_all_notes_for_owner(db, current_user.id, offset, limit)
    except note_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.get("/{note_id}", response_model=note_schema.NoteRead, status_code=status.HTTP_200_OK)
def retrieve_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        note = note_service.get_note_for_owner(db, note_id, current_user.id)

        if not note:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "note not found")

        return note
    except note_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.post("/", response_model=note_schema.NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: note_schema.NoteCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        return note_service.create_note(db, payload, current_user)
    except note_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.patch("/{note_id}", response_model=note_schema.NoteRead, status_code=status.HTTP_200_OK)
def update_note(
    note_id: UUID,
    payload: note_schema.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        note = note_service.get_note_for_owner(db, note_id, current_user.id)

        if not note:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "note not found")

        return note_service.update_note(db, note, payload)
    except note_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        note = note_service.get_note_for_owner(db, note_id, current_user.id)
        if not note:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "note not found")

        return note_service.delete_note(db, note)
    except note_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))
