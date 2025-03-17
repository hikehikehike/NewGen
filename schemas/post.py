from pydantic import BaseModel
from typing import List


class PostCreate(BaseModel):
    """
    Schema for creating a new post.

    - Ensures text validation for post content.

    Attributes:
        text (str): The content of the post.
    """
    text: str

    class Config:
        min_anystr_length = 1  # Ensures that post content is not empty
        anystr_strip_whitespace = True  # Removes leading/trailing whitespace


class PostResponse(BaseModel):
    """
    Schema for returning a post in responses.

    - Used when retrieving posts from the database.
    - Includes the post ID, content, and owner ID.

    Attributes:
        id (int): The unique identifier of the post.
        text (str): The content of the post.
        owner_id (int): The ID of the user who created the post.
    """
    id: int
    text: str
    owner_id: int

    class Config:
        orm_mode = True  # Allows conversion from ORM models to Pydantic models
        from_attributes = True  # Enables ORM compatibility with from_orm()


class PostsResponse(BaseModel):
    """
    Schema for returning multiple posts in a response.

    - Used when retrieving all posts for a user.

    Attributes:
        posts (List[PostResponse]): A list of user posts.
    """
    posts: List[PostResponse]


class DeletePostResponse(BaseModel):
    """
    Schema for post deletion response.

    - Confirms whether a post was successfully deleted.

    Attributes:
        success (bool): Indicates if the deletion was successful.
        message (str): A message describing the result.
    """
    success: bool
    message: str

    class Config:
        orm_mode = True  # Enables conversion from ORM models
