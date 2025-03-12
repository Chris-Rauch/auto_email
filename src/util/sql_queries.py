from sqlmodel import Session, select
from db.models.users import UserBase, User

def queryUser(user: UserBase, session: Session) -> User | None:
    return session.exec(select(User).where(User.username == user.username)).first()

def usernameExists(user: UserBase, session: Session) -> bool:
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    return db_user is not None

def emailExists(user: UserBase, session: Session) -> bool:
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    return db_user is not None
