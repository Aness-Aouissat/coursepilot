from fastapi import APIRouter, HTTPException, Body
from sqlalchemy import select

from app.models import user_models
from app.db.models.users_db import Users
from app.dependencies import SessionDep
from app.services.security import get_password_hash, verify_password

from typing import Annotated

router = APIRouter(prefix = "/v1/auth")

@router.post("/register", response_model=user_models.UsersBase)
async def register(
    session: SessionDep,
    user: Annotated[user_models.SignUp, Body()]
):
    result = await session.execute(select(Users).where(Users.email == user.email))
    user_with_email = result.scalars().first()
    
    if user_with_email:
        raise HTTPException(status_code=409, detail="Email already registered")

    password = user.password
    new_password = get_password_hash(password)

    user_orm = Users(username = user.username, 
                    first_name = user.first_name, 
                    last_name = user.last_name,
                    email = user.email,
                    hashed_password = new_password,
                    age = user.age
                )
    session.add(user_orm)

    await session.commit()
    await session.refresh(user_orm)

    return user_orm

@router.post("/login")
async def login(
    session: SessionDep,
    user_details: user_models.LogIn
):    
    pass
