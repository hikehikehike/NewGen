from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from models.user import User
from schemas.user import UserCreate
from controllers.auth import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


async def signup(user_data: UserCreate, db: AsyncSession):
    """
    Register a new user, hash the password, and return an access token.

    This function performs the following:
    - Hashes the provided password using bcrypt.
    - Creates a new user with the provided email and hashed password.
    - Saves the new user to the database.
    - Generates an access token for the newly created user.

    Args:
        user_data (UserCreate): Data provided by the user containing email and password.
        db (AsyncSession): The database session used to save the user.

    Returns:
        dict: A dictionary containing a success message and the generated access token.

    Raises:
        HTTPException: If the password is not provided or the database operation fails.
    """
    hashed_password = get_password_hash(user_data.password)  # Hash the password
    new_user = User(email=user_data.email, hashed_password=hashed_password)  # Create new user instance

    # Add the new user to the database
    db.add(new_user)
    await db.commit()

    # Generate an access token for the newly created user
    access_token = create_access_token({"sub": str(new_user.id)})

    return {"message": "User created successfully", "access_token": access_token, "token_type": "bearer"}


async def login(user_data: OAuth2PasswordRequestForm, db: AsyncSession):
    """
    Authenticate a user and return an access token if credentials are valid.

    This function performs the following:
    - Retrieves the user by email (username in OAuth2PasswordRequestForm).
    - Verifies the provided password with the stored hashed password.
    - If authentication is successful, generates an access token.
    - If authentication fails, raises an HTTP 401 Unauthorized exception.

    Args:
        user_data (OAuth2PasswordRequestForm): The login credentials (email as username and password).
        db (AsyncSession): The database session used to retrieve the user.

    Returns:
        dict: A dictionary containing the access token if authentication is successful.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
    # Retrieve the user from the database by email (username)
    result = await db.execute(select(User).filter(User.email == user_data.username))
    user = result.scalars().first()

    # If user is not found or password is invalid, raise an error
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate an access token for the authenticated user
    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
