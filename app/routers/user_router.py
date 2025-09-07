from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import user_schema
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[user_schema.UserRead], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    try:
        data = user_service.get_all_users(db, offset, limit)
        return data
    except user_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.get("/{user_id}", response_model=user_schema.UserRead, status_code=status.HTTP_200_OK)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        data = user_service.get_user(db, user_id)

        if not data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

        return data
    except user_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.post("/", response_model=user_schema.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, payload)
    except user_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.patch("/{user_id}", response_model=user_schema.UserRead, status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, payload: user_schema.UserUpdate, db: Session = Depends(get_db)):
    try:
        user = user_service.get_user(db, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

        return user_service.update_user(db, user, payload)
    except user_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = user_service.get_user(db, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

        return user_service.delete_user(db, user)
    except user_service.ConflictError as e:
        return HTTPException(status.HTTP_409_CONFLICT, str(e))
