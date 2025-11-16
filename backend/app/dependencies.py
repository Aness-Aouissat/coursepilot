from typing import Annotated
from fastapi import Depends
from app.db.session import get_async_session, AsyncSession

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]