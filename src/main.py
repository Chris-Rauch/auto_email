from fastapi import FastAPI, HTTPException, Response
from db.models.users import User, UserLogin, UserPublic, UserUpdate, UserCreate
from db.setup import SessionDep, connect_to_db
from util.security import create_access_token, hash_password, verify_password
from util.sql_queries import queryUser, emailExists
from dotenv import dotenv_values

# load config values
config = dotenv_values(".env")
DEBUG = True if config["DEBUG"] == "true" else False

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
    """Add a new user to the 'Users' table. The plaintext password is hashed
    before entering into db.

    Returns:
    A UserPublic, which includes the user_id, username, email, first
    and last. Password hash and the created_at timestamp is ommited.
    If the user already exists, then the existing data is returned.
    """
    # check if user already exists
    existing_user = queryUser(user, session)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    elif emailExists(user,session):
        raise HTTPException(status_code=400, detail="Email already exists")

    # TODO add a function that makes sure email, first and last are less than 255 chars

    # hash password 
    hashed_password = hash_password(user.password)

    # create new user instance
    db_user = User.model_validate(user)
    db_user.password = hashed_password

    # add to users table in emails db
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

@app.post("/login")
def login(user: UserLogin, response: Response, session: SessionDep):
    """Verify user credentials and return an access token.
    """
    # query the user and verify
    db_user = queryUser(user, session)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")
    if not verify_password(user.password_plain, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    # create JWT token and add it to HTTP response
    token = create_access_token(data={"sub": user.username})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not DEBUG,
        samesite="lax"
    )

    responseBody = {"message": "Login successful"}
    if DEBUG:
        responseBody.update({"access_token": token}) # only return access token in debug mode

    return responseBody

"""
from fastapi import Request

@app.get("/protected")
def protected_route(request: Request):
    #An example route that requires a valid JWT token in cookies.
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"message": "You have access!", "user": payload["sub"]}

"""
"""
Methods to add:
    /emails
        - POST, GET, PUT, DELETE
    /users
        - post, put
    /templates
        - post, get, put, delete


"""
