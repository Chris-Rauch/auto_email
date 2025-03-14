from fastapi import HTTPException, Request
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

def create_access_token(data: dict, expires: timedelta | None = None) -> str | None:
    """Generate a JWT access token that expires. 
    Expiration time defaults to expires paramater -> config file value -> 60min.
    Returns the token if successful. Otherwise None.
    """
    # get config data
    secret_key = config.get("SECRET_KEY")
    algorithm = config.get("ALGORITHM")
    config_expires = config.get("ACCESS_TOKEN_EXPIRES_MINUTES")

    # add expire time and encode
    try:
        # verify .env variables
        if not secret_key or not algorithm:
                raise ValueError("Missing SECRET_KEY or ALGORITHM in .env file")
        
        # get the correct expiration time
        if expires is None:

            # caller did not provide a time. Use config file
            if config_expires is not None:
                expires = timedelta(minutes=int(config_expires))

            # neither caller nor config file has a value
            else:
                expires = timedelta(minutes=60) # default to 60
        expiration_time = datetime.utcnow() + expires
        
        # encode data and return
        data_copy = data.copy()
        data_copy.update({"exp":expiration_time})
        token = jwt.encode(data_copy, secret_key, algorithm=algorithm)
    
    # handle errors
    except jwt.ExpiredSignatureError:
        if DEBUG:
            print("JWT Error: Token has expired.")
        return None
    except jwt.InvalidTokenError:
        if DEBUG:
            print("JWT Error: Invalid token.")
        return None
    except ValueError as e:
        if DEBUG:
            print({str(e)})
        return None
    except Exception as e:
        if DEBUG:
            print({str(e)})
        return None
    return token

def verify_access_token(encoded_token: str) -> str | None:
    """Verify JWT access token.
    Return username if verified. Otherwise return None
    """
    # get config data
    algorithm = config.get("ALGORITHM")
    secret_key = config.get("SECRET_KEY")
    if not secret_key or not algorithm:
        if DEBUG:
            print("Missing SECRET_KEY or ALGORITHM in .env file")
        return None

    # decode and grab the username
    try:
        payload = jwt.decode(encoded_token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if not username:
            if DEBUG:
                print("Token missing 'sub' claim. Access token was encrypted incorrectly")
            return None

    # catch errors and return
    except jwt.ExpiredSignatureError:
        if DEBUG:
            print("JWT Error: Token has expired.")
        return None
    except jwt.InvalidTokenError:
        if DEBUG:
            print("JWT Error: Invalid token.")
        return None
    except Exception as e:  # Catch unexpected errors
        if DEBUG:
            print(f"Unexpected Error: {str(e)}")
        return None
    
    if DEBUG:
        print("Access token verified")
    return username
