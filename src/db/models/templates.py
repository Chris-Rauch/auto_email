from sqlmodel import SQLModel, Field

class Templates(SQLModel, table=True):
    template_id: int = Field(primary_key=True, index=True, nullable=False)
    user_id: int = Field(foreign_key='users.user_id', nullable=False)
    var_id: int = Field(foreign_key='vars.var_id', nullable=False)
    name: str = Field(nullable=False)
    subject: str | None = Field(default=None, nullable=True)
    body: str | None = Field(default=None, nullable=True)