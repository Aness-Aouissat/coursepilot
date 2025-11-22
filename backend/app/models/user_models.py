from pydantic import BaseModel, EmailStr
import uuid

class UsersBase(BaseModel):
    first_name:  str
    last_name: str
    age : int
    username: str
    email: EmailStr

class Credentials(BaseModel):
    email: EmailStr
    password: str

class Register(Credentials):
    username: str
    first_name: str
    last_name: str
    age: int

class LogIn(Credentials):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class SignUpResponse(Token):
    user: UsersBase

class TokenData(BaseModel):
    id: uuid.UUID

class UserDelete(BaseModel):
    password: str