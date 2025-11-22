from fastapi import FastAPI
from .api import notes
from .api import users
from app.db.init_db import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()                    
    yield  

def create_app() -> FastAPI:
    
    app = FastAPI(
        title = "CoursePilot",
        version = "1.0.0",
        lifespan=lifespan
    )
    app.include_router(notes.router)
    app.include_router(users.router)
    return app

app = create_app()