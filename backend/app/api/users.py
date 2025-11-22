from fastapi import APIRouter, HTTPException, Response, Body
from sqlalchemy import select

from app.models import user_models
from app.db.models.users_db import Users
from app.dependencies import SessionDep, UserDep
from app.services.security import get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, generate_complete_user_token

from typing import Annotated

router = APIRouter(prefix = "/v1/users")

@router.post("/register", response_model=user_models.SignUpResponse)
async def create_user(
    session: SessionDep,
    user: Annotated[user_models.Register, Body()]
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

    access_token = generate_complete_user_token(user_orm.id)

    return user_models.SignUpResponse(
        user=user_models.UsersBase(
            first_name = user.first_name,
            last_name = user.last_name,
            age = user.age,
            username = user.username,
            email = user.email
        ),
        access_token=access_token, 
        token_type="bearer"
    )

@router.post("/login", response_model=user_models.Token)
async def login(
    session: SessionDep,
    user_login_details: user_models.LogIn
):    
    result = await session.execute(select(Users).where(Users.email == user_login_details.email))
    user = result.scalars().first()
    if not user or not verify_password(user_login_details.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    
    access_token = generate_complete_user_token(user.id)

    return user_models.Token(access_token = access_token, token_type="bearer")    

@router.get("/me", response_model=user_models.UsersBase)
async def get_user_details(
    user: UserDep
):
    return user_models.UsersBase(
        first_name = user.first_name,
            last_name = user.last_name,
            age = user.age,
            username = user.username,
            email = user.email
    )

@router.patch("/me")
async def change_user_details(
    user: UserDep
):
    pass

@router.patch("/me/password")
async def change_password(
    user: UserDep
):
    pass

@router.delete("/me")
async def delete_user(
    user: UserDep,
    session: SessionDep,
    password_confirmation: Annotated[user_models.UserDelete, Body()]
):
    if verify_password(password_confirmation.password, user.hashed_password):
        await session.delete(user)
        await session.commit()
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user")