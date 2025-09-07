from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    firstname: str = Field(min_length=1, max_length=225)
    lastname: str = Field(min_length=1, max_length=225)
    username: str = Field(min_length=1, max_length=225)


class UserRead(UserBase):
    id: UUID
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=1, max_length=225)


class UserUpdate(BaseModel):
    firstname: str | None = Field(default=None, min_length=1, max_length=225)
    lastname: str | None = Field(default=None, min_length=1, max_length=225)
    username: str | None = Field(default=None, min_length=1, max_length=225)
    password: str | None = Field(default=None, min_length=1, max_length=225)
