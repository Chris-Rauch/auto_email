from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True, max_length=255)
    email: str = Field(nullable=False, unique=True, max_length=255)
    first_name: str | None = Field(default=None, nullable=True, max_length=255)
    last_name: str | None = Field(default=None, nullable=True, max_length=255)

class User(UserBase, table=True):
    __tablename__ = "users" #override table name to match mySQL table name
    user_id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False) # TODO utcnow is deprecated. Change for future use

class UserPublic(UserBase):
    user_id: int

class UserCreate(UserBase):
    password_hash: str

class UserUpdate(UserBase):
    username: str | None = Field(default=None, nullable=True, max_length=255)
    email: str | None = Field(default=None, nullable=True, max_length=255)
    pass_hash: str | None = Field(default=None, nullable=True, max_length=255)
