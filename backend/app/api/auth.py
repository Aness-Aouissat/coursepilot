from fastapi import APIRouter 
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix = "/v1/auth")

@router.get("/register")
async def register():
    pass

@router.get("/login")
async def login():
    pass
