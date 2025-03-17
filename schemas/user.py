from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Schema for user registration.

    - Ensures email format validation.
    - Enforces password requirements.

    Attributes:
        email (EmailStr): The user's email address (validated format).
        password (str): The user's password (must meet length requirements).
    """
    email: EmailStr
    password: str

    class Config:
        min_anystr_length = 8  # Enforces a minimum password length of 8 characters
        anystr_strip_whitespace = True  # Removes leading/trailing whitespace


class TokenResponse(BaseModel):
    """
    Schema for authentication token response.

    - Returned when a user successfully logs in.
    - Contains an access token for authentication.

    Attributes:
        access_token (str): The generated JWT access token.
        token_type (str): Token type (typically "bearer").
    """
    access_token: str
    token_type: str
