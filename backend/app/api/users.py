from fastapi import APIRouter, Response, Body

from app.models.user_models import SignUpResponse, Register, UsersBase, Token, LogIn, UserDelete
from app.dependencies import SessionDep, UserDep
from app.services.users_services import (
    register_user_service,
    login_user_service,
    delete_user_service
)

from typing import Annotated

router = APIRouter(prefix = "/v1/users")

@router.post("/register", response_model=SignUpResponse)
async def register_user(
    session: SessionDep,
    user: Annotated[Register, Body()]
):
    return await register_user_service(user, session)

@router.post("/login", response_model=Token)
async def login_user(
    session: SessionDep,
    user_login_details: Annotated[LogIn, Body()]
):    
    return await login_user_service(user_login_details, session)

@router.get("/me", response_model=UsersBase)
async def get_user_details(
    user: UserDep
):
    return UsersBase(
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
    password_confirmation: Annotated[UserDelete, Body()]
):
    await delete_user_service(user, password_confirmation, session)
    return Response(status_code=204)
