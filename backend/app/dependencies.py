from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from sqlalchemy import select

from app.db.session import get_async_session, AsyncSession
from app.services.security import ALGORITHM, SECRET_KEY
from app.models.user_models import TokenData
from app.db.models.users_db import Users

from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    
    result = await session.execute(select(Users).where(Users.id == token_data.id))
    user = result.scalars().first()

    if not user:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=403, detail="Inactive user")
    
    return user

UserDep = Annotated[Users, Depends(get_current_user)]