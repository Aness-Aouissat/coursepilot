from pydantic import BaseModel, EmailStr
import uuid

class UsersBase(BaseModel):
    id: uuid.UUID
    first_name:  str
    last_name: str
    age : int
    username: str
    email: EmailStr
    disabled: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class Credentials(BaseModel):
    email: EmailStr
    password: str

class SignUp(Credentials):
    username: str
    first_name: str
    last_name: str
    age: int

class LogIn(Credentials):
    pass

