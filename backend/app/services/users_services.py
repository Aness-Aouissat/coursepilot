from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.users_db import Users
from app.models.user_models import SignUpResponse, Register, UsersBase, LogIn, Token, UserDelete
from app.services.security import (
    get_password_hash, 
    generate_complete_user_token, 
    verify_password
)

async def register_user_service(
    data: Register,
    session: AsyncSession
) -> SignUpResponse:
    result = await session.execute(select(Users).where(Users.email == data.email))
    existing = result.scalars().first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hashed = get_password_hash(data.password)

    user_orm = Users(username = data.username, 
                    first_name = data.first_name, 
                    last_name = data.last_name,
                    email = data.email,
                    hashed_password = hashed,
                    age = data.age)
    session.add(user_orm)

    await session.commit()
    await session.refresh(user_orm)

    token = generate_complete_user_token(user_orm.id)

    return SignUpResponse(
        user=UsersBase(
            first_name=data.first_name,
            last_name=data.last_name,
            age=data.age,
            username=data.username,
            email=data.email
        ),
        access_token=token,
        token_type="bearer"
    )

async def login_user_service(
    user_login_details: LogIn,
    session: AsyncSession
) -> Token:
    result = await session.execute(select(Users).where(Users.email == user_login_details.email))
    user = result.scalars().first()
    if not user or not verify_password(user_login_details.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    
    token = generate_complete_user_token(user.id)

    return Token(access_token = token, token_type="bearer")    

async def delete_user_service(
    user: Users, 
    password_confirmation: UserDelete,
    session: AsyncSession
):
    if verify_password(password_confirmation.password, user.hashed_password):
        await session.delete(user)
        await session.commit()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user")