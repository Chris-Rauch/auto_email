import util
from fastapi import FastAPI, HTTPException, Request, Response
from db.models.contacts import Contacts
from db.models.schedule import Schedule, ScheduleCreate, ScheduleCreateFromList
from db.models.templates import TemplateBase, Templates
from db.models.users import User, UserLogin, UserPublic, UserUpdate, UserCreate
from db.setup import SessionDep, connect_to_db
import util.helpers
from util.security import create_access_token, hash_password, verify_access_token, verify_password
from util.sql_queries import get_contacts_by_email, getTemplate, getUserId, queryUser, emailExists, templateExists
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

"""ADD USER"""
@app.post("/user", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    """Add a new user to the database.
    Returns the newly assigned user id. Also returns the username and email for
    verification.
    """
    # check if user already exists
    existing_user = queryUser(user, session)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    elif emailExists(user,session):
        raise HTTPException(status_code=400, detail="Email already exists")

    # TODO add a function that makes sure email, first and last are less than
    # 255 chars

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

"""UPDATE USER""" 
@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    users_db = session.get(User, user_id)
    if not users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    user_data = user.model_dump(exclude_unset=True)
    users_db.sqlmodel_update(user_data)
    session.add(users_db)
    session.commit()
    session.refresh(users_db)
    return users_db

# TODO remove vars table from db
"""CREATE A TEMPLATE"""
@app.post("/template", response_model=TemplateBase)
def create_template(template: TemplateBase, request: Request, session: SessionDep):
    """Adds a template to the DB. Requires authorization.
    """
    # verify access token
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    jwt_token = auth_header.split(" ")[1]
    username = verify_access_token(jwt_token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # check if template already exists
    existing_template = templateExists(template, session)
    if existing_template is not None:
        raise HTTPException(status_code=409, detail="Template already exists")

    # add to db
    db_template = Templates.model_validate(template)
    session.add(db_template)
    session.commit()
    session.refresh(db_template)
    return db_template

"""ADD CONTACT"""
@app.post("/contact")
def add_contact():
    pass

"""ADD EMAIL TO SCHEDULE"""
#TODO change db: email_id -> schedule ID
@app.post("/schedule")
def schedule_email(schedule: ScheduleCreateFromList, request: Request, session: SessionDep):
    """Adds emails and contacts to the db.
    """
    # authenticate the reuqest's JWT token and get user id
    username = util.helpers.auth_user(request)
    user_id = getUserId(username, session)

    # get template from db
    db_template = getTemplate(schedule.template_id, session)
    if not db_template:
        raise HTTPException(status_code=409, detail="Template does not exist")

    # verify user input
    util.helpers.check_for_vars(schedule.contacts, \
            db_template.subject, \
            db_template.body)

    # generate send_times
    send_times = util.helpers.generate_send_times(schedule.when, \
            len(schedule.contacts), \
            schedule.start_time, \
            schedule.end_time)
    
    # add contacts to db
    contact_entries = [Contacts.model_validate(contact) for contact in schedule.contacts]
    session.add_all(contact_entries) # TODO test what this does. I need contact_entries to be updated with auto generated id's
    for contact in contact_entries:
        session.refresh(contact)

    # create schedule entries and add to db
    schedule_entry = []
    for i, contact in enumerate(contact_entries):
        entry = ScheduleCreate(
            user_id=user_id,
            contact_id=contact.contact_id,
            send_time=send_times[i],
            template_id=db_template.template_id
        )
        db_entry = Schedule.model_validate(entry)
        schedule_entry.append(db_entry)
    
    session.add_all(schedule_entry)
    session.commit()


"""CHECK SCHEDULE"""
@app.get("/schedule")
def check_scheduled_emails(schedule: Schedule, request: Request, session: SessionDep):
    pass

"""VERIFY CREDENTIALS"""
@app.post("/login")
def login(user: UserLogin, response: Response, session: SessionDep):
    """Verify user credentials and return an access token. 
    After login when trying to access a resource via the access token, it should
    exist in the header as: { Authorization: "Bearer <token>" }
    """
    # query the user and verify
    db_user = queryUser(user, session)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")
    if not verify_password(user.password_plain, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    # create JWT token and add it to HTTP response cookie header
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
