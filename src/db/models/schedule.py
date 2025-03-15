from datetime import datetime
from sqlmodel import SQLModel, Field

from db.models.contacts import ContactsBase

class ScheduleBase(SQLModel):
    send_time: datetime = Field(nullable=False)
    template_id: int = Field(foreign_key='templates.template_id', index=True, nullable=False)

class Schedule(ScheduleBase, table=True):
    schedule_id: int = Field(primary_key=True, index=True, nullable=True)
    user_id: int = Field(foreign_key='users.user_id', index=True, nullable=False)
    contact_id: int = Field(foreign_key='contacts.contact_id', index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    status: str  = Field(default='pending', nullable=False)

class ScheduleCreate(ScheduleBase):
    user_id: int = Field(foreign_key='users.user_id', index=True, nullable=False)
    contact_id: int = Field(foreign_key='contact.contact_id', index=True, nullable=False)

class ScheduleCreateFromList(ScheduleBase):
    contacts: list[ContactsBase]
    when: str # randomize, burst, timeframe
    start_time: datetime | None
    end_time: datetime | None


