"""Configuration file for Emails app. Purpose is to congregate predetermined
variable values into one place. Should help reduce amount of arguments
throughout the program
"""
from passlib.context import CryptContext

# JWT (JSON Web Token authentication)
jwt = dict(
    secret_key = "My_super_secret_key"
    algorithm = "HS256"
    expire = 30 # expire time in minutes
)
# Don't know what this is yet
context = CryptContext(schemes=["bcrypt"], deprecated="auto")
