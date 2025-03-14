"""Logic that should be in the main app. This file should help make main more
readable.

Throws HTTP Exceptions
"""

from datetime import datetime
from fastapi import HTTPException, Request
from util.security import verify_access_token

def auth_user(request: Request):
    """Extracts and verifies the token from Authorization header.
    Returns the username encrypted within the token.
    """
    # verify access token
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    jwt_token = auth_header.split(" ")[1]
    username = verify_access_token(jwt_token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return username

def check_for_vars(contacts: list[dict], subject: str, body: str) -> bool:
    """Ensures data integrity by verifying user input. Vars can be present in a
    template's subject or body field and are identified with a leading '#'. For 
    example, an email's subject line can read 'Greetings from #name'. In
    this case, #name is a var and the contact should have a corresponding var
    named 'name'.
    Returns true if all appropriate data is present.
    """
    # based on the template, get the required variables
    all_words = subject.split(" ") + body.split(" ")
    required_vars = {word[1:] for word in all_words if word.startswith('#') and len(word) > 1}
        
    # check that all contacts contain required vars
    for contact in contacts:
        missing_vars = required_vars - contact.keys()
        extra_vars = contact.keys() - required_vars
        if missing_vars:
            raise HTTPException(status_code=409, detail=f"Missing contact \
                     variables {missing_vars}")
        if extra_vars:
            raise HTTPException(status_code=409, detail=f"Too many contact \
                     variables {extra_vars}")
    
    return True
    
def generate_send_times(when: str, size: int, \
            start: datetime, stop: datetime | None) -> list[datetime]:
    """Create a list of datetimes for emails
    """
    if size <= 0:
        raise HTTPException(status_code=409, detail="Size must be greater than zero")

    match when:
        case "burst":
            # send emails all at once
            times = [times.replace() for _ in range(size)]

        case "timeframe":
            # Send emails out spaced evenly through [start,end]
            if stop is None:
                raise HTTPException(status_code=409, detail="Server Error. \
                        Unable to disperse emails across a timeframe")
            if start >= stop:
                raise HTTPException(status_code=409, detail="Start time must be\
                         before stop time")
            step = (stop-start) / size
            times = [start + (i * step) for i in range(size)]
        case _:
            raise HTTPException(status_code=409, detail="Invalid 'when' argument")
    return times