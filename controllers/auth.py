from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends

# Secret key and algorithm used for JWT encoding/decoding
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time (30 minutes)

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current authenticated user from the provided JWT token.

    - This function extracts user information from the access token.
    - If the token is invalid or expired, it raises an HTTP 401 Unauthorized error.

    Parameters:
        token (str): The JWT token provided in the request header.

    Returns:
        dict: The decoded payload from the token containing user details.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generate a JWT access token.

    - This function encodes a dictionary of user-related data into a JWT.
    - It also includes an expiration timestamp for security.

    Parameters:
        data (dict): The user-related data to encode into the token.
        expires_delta (Optional[timedelta]): Custom expiration time for the token.

    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Add expiration time to the token payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plaintext password matches the hashed password.

    Parameters:
        plain_password (str): The raw password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    - This function securely hashes a plaintext password before storing it in the database.

    Parameters:
        password (str): The plaintext password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def decode_access_token(token: str):
    """
    Decode and validate a JWT access token.

    - This function attempts to decode the JWT token and return the payload.
    - If decoding fails (e.g., invalid token or expired), it returns None.

    Parameters:
        token (str): The JWT token to decode.

    Returns:
        dict | None: The decoded payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
