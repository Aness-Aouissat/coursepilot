from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from dotenv import load_dotenv

import jwt
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    """
    To be used in user log in. The input password will be verified
    against the hashed password stored in the database before granting 
    the user access.
    """
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    To be used in user registration. The input password will be 
    hashed before being stored in the database to be used for future
    verifications.
    """
    return password_hash.hash(password)

def create_access_token():
    pass

def decode_token():
    pass


