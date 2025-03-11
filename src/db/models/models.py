"""Defines models for the 4 mySQL tables I will be using in this project:
  - Schedule
  - Templates
  - Vars
  - Users
"""

from sqlmodel import Field, SQLModel
from datetime import datetime

class Templates(SqlModel, table=True):
    template_id: int = Field(primary_key=True, index=True, nullable=False)
    user_id: int = Field(foreign_key='users.user_id', nullable=False)
    var_id: int = Field(foreign_key='vars.var_id', nullable=False)
    name: str = Field(nullable=False)
    subject: str | None = Field(default=None, nullable=True)
    body: str | None = Field(default=None, nullable=True)
    
class Vars(SQLModel, table=true):
    var_id: int Field(primary_key=True, index=True, nullable=False)
    user_id: int Field(foreign_key='users.user_id', nullable=False)
    var_key: str Field(nullable=False, max_length=255)
    var_value: str Field(nullable=False, max_length=255)
