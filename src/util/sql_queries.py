from sqlmodel import Session, select
from db.models.users import UserBase, User

def queryUser(user: UserBase, session: Session) -> User | None:
    return session.exec(select(User).where(User.username == user.username)).first()