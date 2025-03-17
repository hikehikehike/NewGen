from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base import Base


class User(Base):
    """
    Represents a user in the database.

    - Stores user information, including email and hashed password.
    - Establishes a one-to-many relationship with the `Post` model.

    Attributes:
        id (int): Primary key for the user.
        email (str): Unique email address of the user (indexed for fast lookups).
        hashed_password (str): Securely stored hashed password.
        posts (List[Post]): Relationship to the `Post` model, linking posts created by this user.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)  # Auto-incrementing primary key
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True,
                                       nullable=False)  # Unique email with an index
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)  # Securely hashed password

    # One-to-many relationship: A user can have multiple posts
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="owner",
        lazy="select",  # Fetch posts only when accessed
        cascade="all, delete-orphan"  # Delete posts if the user is deleted
    )
