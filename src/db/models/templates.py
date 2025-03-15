from sqlmodel import SQLModel, Field

class TemplateBase(SQLModel):
    name: str = Field(nullable=False)
    subject: str = Field(nullable=False)
    body: str = Field(nullable=False)

class Templates(TemplateBase, table=True):
    template_id: int = Field(primary_key=True, index=True, nullable=False)
    user_id: int = Field(foreign_key='users.user_id', nullable=False)


