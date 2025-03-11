from sqlmodel import SQLModel, Field

class Vars(SQLModel, table=True):
    var_id: int = Field(primary_key=True, index=True, nullable=False)
    user_id: int = Field(foreign_key='users.user_id', nullable=False)
    var_key: str = Field(nullable=False, max_length=255)
    var_value: str = Field(nullable=False, max_length=255)