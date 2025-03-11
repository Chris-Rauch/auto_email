import datetime
from sqlmodel import SQLModel, Field

class Schedule(SQLModel, table=True):
    email_id: int = Field(primary_key=True, index=True, nullable=False)
    template_id: int = Field(foreign_key='templates.template_id', index=True, nullable=False)
    send_time: datetime = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    status: str | None = Field(default='pending', nullable=True)
