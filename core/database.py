import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database connection URL retrieved from environment variables (for flexibility in different environments)
# If the environment variable is not set, a default PostgreSQL connection string is used.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://myuser:mypassword@db:5432/mydatabase")

# Create an asynchronous SQLAlchemy engine for database interactions
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Create a session factory that produces asynchronous database sessions
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, future=True)


async def get_db():
    """
    Dependency function to provide a database session.

    - This function provides an async database session using SQLAlchemy.
    - The session is automatically closed after the request is processed.
    - It is used as a dependency in FastAPI endpoints that require database access.

    Yields:
        AsyncSession: An active SQLAlchemy database session.
    """
    async with SessionLocal() as session:
        yield session
