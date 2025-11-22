from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from dotenv import load_dotenv

import jwt
import os
import uuid

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    copy_of_data = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    copy_of_data.update({"exp": expire})
    access_token = jwt.encode(copy_of_data, SECRET_KEY, algorithm=ALGORITHM)

    return access_token

def generate_complete_user_token(user_id: uuid.UUID):
    sub = {"sub": str(user_id)}
    exp = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(sub, exp) 

    return access_token