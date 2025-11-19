from .session import engine, Base
from app.db.models.users_db import Users
from app.db.models.notes_db import Notes

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)