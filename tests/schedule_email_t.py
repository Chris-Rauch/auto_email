import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi import HTTPException, Request
from db.setup import SessionDep
from db.models.contacts import Contacts
from db.models.schedule import ScheduleCreateFromList
from util.security import verify_access_token
from util.sql_queries import getTemplate, getUserId
from datetime import datetime
from starlette.types import Scope

"""TEST DATA"""
schedule_test = ScheduleCreateFromList(
    send_time=datetime.utcnow(),
    template_id=1,
    contacts=
    [
        {
            "email":"chrisrauch2@aol.com",
            "user_id":1,
            "vars": 
            {
                "amount": 55.01,
                "day": "Thursday"
            },
            "company": "Tesla",
            "first_name": None,
            "last_name": "Kelly",
            "notes": None
        },
        {
            "email": "john.doe@example.com",
            "user_id": 2,
            "vars": {
                "amount": 120.75,
                "day": "Monday"
            },
            "company": "Apple",
            "first_name": "John",
            "last_name": "Doe",
            "notes": "VIP customer"
        },
        {
            "email": "jane.smith@example.com",
            "user_id": 3,
            "vars": {
                "amount": 89.99,
                "day": "Wednesday"
            },
            "company": "Microsoft",
            "first_name": "Jane",
            "last_name": "Smith",
            "notes": None
        },
        {
            "email": "michael.brown@example.com",
            "user_id": 4,
            "vars": {
                "amount": 45.50,
                "day": "Friday"
            },
            "company": "Google",
            "first_name": "Michael",
            "last_name": "Brown",
            "notes": "Frequent buyer"
        },
        {
            "email": "sarah.jones@example.com",
            "user_id": 5,
            "vars": {
                "amount": 150.25,
                "day": "Tuesday"
            },
            "company": "Amazon",
            "first_name": "Sarah",
            "last_name": "Jones",
            "notes": "Prefers email contact"
        },
        {
            "email": "david.wilson@example.com",
            "user_id": 6,
            "vars": {
                "amount": 32.10,
                "day": "Sunday"
            },
            "company": "Facebook",
            "first_name": "David",
            "last_name": "Wilson",
            "notes": None
        }
    ],
    send_type="burst",
    start_time=None,
    end_time=None
)

# Manually construct a request scope
scope: Scope = {
    "type": "http",
    "method": "POST",
    "path": "/test",
    "headers": [(b"authorization", b"Bearer mytoken")],
    "query_string": b"",
    "scheme": "http",
    "client": ("127.0.0.1", 8000),
    "server": ("127.0.0.1", 8000),
}

# Create the request object
request = Request(scope)
session = SessionDep


def schedule_email(schedule: ScheduleCreateFromList, request: Request, session: SessionDep):
    """Adds emails to the schedule. Also add contacts to the db.
    """
    # verify access token
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")"
    
    
    jwt_token = auth_header.split(" ")[1]
    username = verify_access_token(jwt_token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid access token")
    """
    # get user id
    user_id = getUserId("studmuffin1314", session)

    # get template
    db_template = getTemplate(schedule.template_id, session)
    if not db_template:
        raise HTTPException(status_code=409, detail="Template does not exist")

    # based on the template, get the required variables
    all_text = db_template.subject.split(" ") + db_template.body.split(" ")
    variable_keys = []
    for word in all_text:
        if word.startswith("#"):
            variable_keys.append(word)
        
    # data integrity
    # verify that contacts have the associated variables for the template
    for contact in schedule.contacts:
        for key in contact.keys():
            if key not in variable_keys:
                raise HTTPException(status_code=409, detail="Missing contact info")

    # create contact entries to add to database
    contact_entries = []
    for contact in schedule.contacts:
        entry = Contacts(
            user_id=user_id,
            email=contact.email,
            vars=contact.vars,
            company=contact.company,
            first_name=contact.first_name,
            last_name=contact.last_name,
            notes=contact.notes
        )

schedule_email(schedule_test, scope, session)