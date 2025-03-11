from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True, max_length=255)
    email: str = Field(nullable=False unique=True, max_length=255)
    first_name: str | None = Field(default=None, nullable=True, max_length=255)
    last_name: str | None = Field(default=None, nullable=True, max_length=255)

class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True, index=True, nullable=False)
    pass_hash: str = Field(nullable=False max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class UserPublic(UserBase):
    user_id: int

class UserCreate(UserBase):
    pass_hash: str

class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    pass_hash: str | None = None
