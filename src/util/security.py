from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import dotenv_values
import jwt

# load config file
config = dotenv_values(".env")
DEBUG = True if config["DEBUG"] == "true" else False

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    """Generate a JWT access token that expires. Expiration time defaults to
    the value in minutes in the .env file. Expi
    """
    # set expiration time 
    if not expires:
        expires = datetime.utcnow() + timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRES_MINUTES"]))

    # encode data and return
    data_copy = data.copy()
    data_copy.update({"exp":expires})
    return jwt.encode(data_copy, config["SECRET_KEY"], algorithm=config["ALGORITHM"])


def verify_access_token(encoded_data: str) -> bool:
    """Verify JWT access token"""
    config = dotenv_values(".env")
    try:
        jwt.decode(encoded_data, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
    except jwt.ExpiredSignatureError as e:
        if DEBUG:
            print(str(e))
        return False
    except jwt.InvalidTokenError as e:
        if DEBUG:
            print(str(e))
        return False
    else:
        if DEBUG:
            print("Access token verified")
        return True
