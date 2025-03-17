from fastapi import FastAPI
from routers import users, posts
from core.database import engine
from models.base import Base

# Create an instance of the FastAPI application
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    """
    Event handler that runs on application startup.

    - This function ensures that the database schema is created before the application starts.
    - It uses SQLAlchemy's `run_sync(Base.metadata.create_all)` to create tables if they do not exist.
    - Runs inside an asynchronous context using `engine.begin()`.

    Note:
        This is useful for initializing the database schema when the application starts,
        but in production, migrations should be used instead (e.g., Alembic).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Include routers for different API endpoints
app.include_router(users.router)  # User-related endpoints (signup, login)
app.include_router(posts.router)  # Post-related endpoints (CRUD operations)
