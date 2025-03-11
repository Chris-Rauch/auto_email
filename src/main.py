from fastapi import FastAPI, HTTPException

# mySQL models
from db.models.users import User, UserPublic, UserUpdate
from db.models.users import UserCreate
from db.setup import SessionDep, connect_to_db

# init
def lifespan(app: FastAPI):
    """When the app first launches we need to a session to interact with the db.
    """
    connect_to_db()
    yield
    # stuff that executes after the life of the app goes here

app = FastAPI(lifespan=lifespan)

"""DATA ENTRY"""
@app.post("/create_user", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    """Add a new user to the 'Users' table. 
    Returns the user's id. If the user already exists, than the existing id
    entry is returned.
    """
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

"""DATA UPDATE"""
@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    users_db = session.get(User, user_id)
    if not users_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    user_data = user.model_dump(exclude_unset=True)
    users_db.sqlmodel_update(user_data)
    session.add(users_db)
    session.commit()
    session.refresh(users_db)
    return users_db

@app.get("/login")
def login():
    """login - Verify user credentials against 'emails' mySQL database. Return
    some sort of verification key.
    """
    return {"message": "Trying to log in..."}

