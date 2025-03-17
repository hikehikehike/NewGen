from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Post(Base):
    """
    Represents a post in the database.

    - Stores text content and the ID of the user who created it.
    - Establishes a many-to-one relationship with the `User` model.

    Attributes:
        id (int): Primary key for the post.
        text (str): The content of the post.
        owner_id (int): Foreign key referencing the user who created the post.
        owner (User): Relationship to the `User` model.
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)  # Auto-incrementing primary key
    text: Mapped[str] = mapped_column(Text, nullable=False)  # Post content (text format)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"),
                                          nullable=False)  # Foreign key linking to `User`

    # Many-to-one relationship: Each post belongs to a single user
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
        lazy="select"  # Fetch user details only when accessed
    )
