from pydantic import BaseModel, EmailStr

class Credentials(BaseModel):
    email : EmailStr
    password: str

class Regsiter(BaseModel):
    pass

class LogIn(Credentials):
    pass
