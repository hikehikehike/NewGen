from fastapi import Depends, APIRouter
from controllers.auth import get_current_user
from core.database import get_db
from schemas.post import PostsResponse, DeletePostResponse
from controllers.post_service import add_post_to_db_and_cache, get_user_posts_from_cache_or_db, \
    delete_post_from_db_and_cache
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.post import PostCreate
from fastapi import Request

router = APIRouter()


@router.post("/addpost/")
async def add_post(
        post: PostCreate,
        request: Request,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Endpoint to add a new post for the current user.

    This endpoint allows the user to create a new post. It checks the size of the payload
    to ensure that it does not exceed the 1 MB limit. The post is then saved in the database
    and added to the cache for quick retrieval in future requests.

    Parameters:
        post (PostCreate): The data for the new post (includes text).
        request (Request): The HTTP request object used to check the payload size.
        current_user (dict): The currently authenticated user, obtained from the `get_current_user` dependency.
        db (AsyncSession): The database session used to interact with the database.

    Returns:
        dict: A dictionary containing the newly created post's ID.

    Raises:
        HTTPException: If the payload size exceeds 1 MB, the request will be rejected.
    """
    user_id = int(current_user.get("sub"))

    # Call the service to create the post and update the cache
    new_post = await add_post_to_db_and_cache(post, user_id, db, request)

    return {"postID": new_post.id}


@router.get("/getposts/", response_model=PostsResponse)
async def get_posts(
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to retrieve all posts for the current user.

    This endpoint fetches the user's posts either from the cache or from the database.
    If the posts are found in the cache, they are returned directly. If not, it retrieves them
    from the database and stores them in the cache for future requests.

    Parameters:
        current_user (dict): The currently authenticated user, obtained from the `get_current_user` dependency.
        db (AsyncSession): The database session used to interact with the database.

    Returns:
        dict: A dictionary containing a list of posts for the authenticated user.

    Raises:
        HTTPException: If no posts are found for the user, a 404 error is raised.
    """
    user_id = int(current_user.get("sub"))

    # Fetch posts from the cache or database
    posts = await get_user_posts_from_cache_or_db(user_id, db)

    return {"posts": posts}


@router.delete("/deletepost/{post_id}", response_model=DeletePostResponse)
async def delete_post(
        post_id: int,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to delete a post by ID for the current user.

    This endpoint allows the user to delete a post they have created. The post is removed
    from both the database and the cache. If the post does not exist or does not belong to
    the user, an error is raised.

    Parameters:
        post_id (int): The ID of the post to be deleted.
        current_user (dict): The currently authenticated user, obtained from the `get_current_user` dependency.
        db (AsyncSession): The database session used to interact with the database.

    Returns:
        dict: A success message indicating the post was deleted.

    Raises:
        HTTPException: If the post is not found or does not belong to the current user, a 404 error is raised.
    """
    user_id = int(current_user.get("sub"))

    # Delete the post from the database and cache
    await delete_post_from_db_and_cache(post_id, user_id, db)

    return {"success": True, "message": "Post deleted successfully"}
