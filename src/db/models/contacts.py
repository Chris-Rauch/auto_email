
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON


class ContactsBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    user_id: int = Field(foreign_key='users.user_id', nullable=False)
    vars: dict | None= Field(default=None, sa_column=Column(JSON)) 
    company: str | None= Field(default=None, nullable=True, max_length=255) 
    first_name: str | None= Field(default=None, nullable=True, max_length=255) 
    last_name: str | None= Field(default=None, nullable=True, max_length=255) 
    notes: str | None= Field(default=None, nullable=True) 

class Contacts(ContactsBase, table=True):
    contact_id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False) # TODO utcnow is deprecated. Change for future use
