"""File for creating the SQLModel engine (underneath it's actually a SQLAlchemy
engine) and is what holds connections to the db. This is what connects the
python code to mySQL server.
"""
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "mysql://chris@localhost:3306/emails"

# create the engine
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)

def connect_to_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# type alias for Session. Injects a session into the session param by calling 
# get_session 
SessionDep = Annotated[Session, Depends(get_session)]

