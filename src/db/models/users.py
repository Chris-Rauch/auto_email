from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True, max_length=255)

class User(UserBase, table=True):
    __tablename__ = "users" #override table name to match mySQL table name
    email: str = Field(nullable=False, unique=True, max_length=255)
    first_name: str | None = Field(default=None, nullable=True, max_length=255)
    last_name: str | None = Field(default=None, nullable=True, max_length=255)
    user_id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False) # TODO utcnow is deprecated. Change for future use

class UserPublic(UserBase):
    user_id: int
    email: str = Field(nullable=False, unique=True, max_length=255)

class UserCreate(UserBase):
    email: str = Field(nullable=False, unique=True, max_length=255)
    first_name: str | None = Field(default=None, nullable=True, max_length=255)
    last_name: str | None = Field(default=None, nullable=True, max_length=255)
    password: str = Field(nullable=False, max_length=255) # plaintext password

class UserUpdate(UserBase):
    username: str | None = Field(default=None, nullable=True, max_length=255)
    email: str | None = Field(default=None, nullable=True, max_length=255)
    pass_hash: str | None = Field(default=None, nullable=True, max_length=255)

class UserLogin(UserBase):
    password_plain: str
