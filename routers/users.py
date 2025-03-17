from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import TokenResponse, UserCreate
from core.database import get_db
from controllers.user_service import signup, login

router = APIRouter()


@router.post("/signup/")
async def signup_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Endpoint for user registration.

    This endpoint allows users to sign up by providing an email and password.
    The password is securely hashed before storing it in the database.
    After successful registration, an access token is generated and returned to the user.

    Parameters:
        user (UserCreate): The user data containing email and password.
        db (AsyncSession): The database session used to store user data.

    Returns:
        dict: A response containing a success message and an access token.

    Raises:
        HTTPException: If the password is not provided or the database operation fails.
    """
    return await signup(user, db)


@router.post("/login/", response_model=TokenResponse)
async def login_user(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Endpoint for user login.

    This endpoint allows users to log in by providing their email and password.
    The password is verified against the stored hashed password.
    If authentication is successful, an access token is generated and returned.
    If authentication fails, an error response is returned.

    Parameters:
        data (OAuth2PasswordRequestForm): The login credentials (username as email and password).
        db (AsyncSession): The database session used to retrieve user data.

    Returns:
        dict: A response containing the access token if authentication is successful.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
    return await login(data, db)
