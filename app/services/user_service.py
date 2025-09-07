from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas import user_schema
from app.utils.security import hash_password
from app.utils.validators import validate_password


class ConflictError(Exception): ...


def create_user(db: Session, payload: user_schema.UserCreate):
    try:
        validate_password(payload.password)

        hashed_password = hash_password(payload.password)

        user = UserModel(
            firstname=payload.firstname,
            lastname=payload.lastname,
            username=payload.username,
            password=hashed_password,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def get_user(db: Session, user_id: UUID):
    return db.get(UserModel, user_id)


def update_user(db: Session, user_model: UserModel, payload: user_schema.UserUpdate):
    data = payload.model_dump(exclude_unset=True)
    pwd = data.get("password")

    if pwd:
        validate_password(pwd)
        data["password"] = hash_password(pwd)

    for key, value in data.items():
        setattr(user_model, key, value)
    try:
        db.commit()
        db.refresh(user_model)
        return user_model
    except IntegrityError as e:
        db.rollback()
        raise ConflictError("username already exist") from e
    except Exception:
        db.rollback()
        raise


def get_all_users(db: Session, offset: int = 0, limit: int = 10):
    stmt = (
        select(UserModel)
        .order_by(desc(UserModel.joined_at), desc(UserModel.id))
        .offset(offset)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


def delete_user(db: Session, user_model: UserModel):
    try:
        db.delete(user_model)
        db.commit()
        return None
    except Exception:
        db.rollback()
        raise
