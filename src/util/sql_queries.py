from dotenv import dotenv_values
from sqlalchemy import Sequence
from sqlmodel import Session, select
from db.models.contacts import Contacts
from db.models.templates import TemplateBase, Templates
from db.models.users import UserBase, User
from sqlalchemy.exc import SQLAlchemyError

# load config file
config = dotenv_values(".env")
DEBUG = True if config["DEBUG"] == "true" else False

def queryUser(user: UserBase, session: Session) -> User | None:
    try:
        db_user = session.exec(select(User).where(User.username == user.username)).first()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return None
    return db_user

def usernameExists(user: UserBase, session: Session) -> bool:
    try:
        db_user = session.exec(select(User).where(User.username == user.username)).first()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return False
    return db_user is not None

def emailExists(user: UserBase, session: Session) -> bool:
    try:
        db_user = session.exec(select(User).where(User.email == user.email)).first()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return False
    return db_user is not None

def templateExists(template: TemplateBase, session: Session):
    try:
        db_template = session.exec(select(Templates).where(Templates.name == template.name)).first()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return False
    return db_template is not None

def getUserId(username: str, session: Session):
    try:
        id = session.exec(select(User.user_id).where(User.username == username)).first()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return False
    return id

def getTemplate(id: int, session: Session):
    try:
        db_template = session.exec(select(Templates).where(Templates.template_id == id)).first()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return False
    return db_template 

def get_contacts_by_email(emails: list[str], session: Session) -> Sequence[Contacts] | None:
    try:
        db_contacts = session.exec(select(Contacts).where(Contacts.email.in_(emails)))
        return db_contacts.all()
    except SQLAlchemyError as e:
        if DEBUG:
            print(f"Database error: {str(e)}")
        return None