from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.post import Post
from schemas.post import PostCreate, PostResponse
from cachetools import TTLCache
from fastapi import Request
from fastapi import HTTPException, status

# Initialize a TTL (Time To Live) cache with a max size of 100 and TTL of 5 minutes.
cache = TTLCache(maxsize=100, ttl=300)


async def add_post_to_db_and_cache(post: PostCreate, user_id: int, db: AsyncSession, request: Request):
    """
    Create a new post in the database and update the cache if it exists.

    This function performs the following:
    - Checks if the request payload size exceeds 1 MB and raises an error if so.
    - Creates a new post using the provided `post` data and the `user_id`.
    - Adds the new post to the database.
    - If there are cached posts for the user, it appends the new post to the cache.

    Parameters:
        post (PostCreate): The post data (text) provided by the user to create a new post.
        user_id (int): The ID of the user who is creating the post.
        db (AsyncSession): The database session used to interact with the database.
        request (Request): The HTTP request object used to determine the request body size.

    Returns:
        Post: The newly created post object.

    Raises:
        HTTPException: If the payload size exceeds 1 MB.
    """
    body_size = len(await request.body())
    if body_size > 1_000_000:  # Check if the payload size is larger than 1 MB
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Payload too large")

    # Create and save the new post in the database
    new_post = Post(text=post.text, owner_id=user_id)
    db.add(new_post)
    await db.commit()

    # Update the cache if it exists
    cached_posts = cache.get(user_id)
    if cached_posts:
        cached_posts.append(PostResponse.from_orm(new_post))  # Add the new post to the cache

    return new_post


async def get_user_posts_from_cache_or_db(user_id: int, db: AsyncSession):
    """
    Retrieve all posts for a given user from the cache or from the database.

    This function first checks if the user's posts are already cached. If they are, it returns them directly.
    If not, it fetches the posts from the database and stores them in the cache for future requests.

    Parameters:
        user_id (int): The ID of the user whose posts are being fetched.
        db (AsyncSession): The database session used to retrieve posts from the database.

    Returns:
        List[PostResponse]: A list of PostResponse objects representing the user's posts.

    Raises:
        HTTPException: If no posts are found for the user.
    """
    cached_posts = cache.get(user_id)
    if cached_posts:
        cached_posts = [PostResponse.from_orm(post) for post in cached_posts]  # Convert cached posts to PostResponse
        return cached_posts

    # Fetch from the database if not in the cache
    result = await db.execute(select(Post).filter(Post.owner_id == user_id))
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No posts found")  # If no posts found, raise an error

    # Store posts in cache for future use
    cache[user_id] = posts  # Save posts to cache

    return [PostResponse.from_orm(post) for post in posts]  # Return the posts as PostResponse objects


async def delete_post_from_db_and_cache(post_id: int, user_id: int, db: AsyncSession):
    """
    Delete a post by its ID, both from the database and the cache.

    This function performs the following:
    - Retrieves the post by its ID and verifies that it belongs to the current user.
    - Deletes the post from the database if it exists and belongs to the user.
    - If the post exists in the cache, it is also removed from the cached data.

    Parameters:
        post_id (int): The ID of the post to be deleted.
        user_id (int): The ID of the user who wants to delete the post.
        db (AsyncSession): The database session used to interact with the database.

    Returns:
        bool: `True` if the post was successfully deleted, `False` if the post was not found or not owned by the user.

    Raises:
        HTTPException: If the post is not found or not owned by the user.
    """
    # Retrieve the post to be deleted
    post = await db.execute(select(Post).filter(Post.id == post_id, Post.owner_id == user_id))
    post = post.scalars().first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or not owned by the user")

    # Delete the post from the database
    await db.delete(post)
    await db.commit()

    # Remove the post from the cache if it exists
    cached_posts = cache.get(user_id)
    if cached_posts:
        cached_posts = [p for p in cached_posts if p.id != post_id]  # Remove the deleted post from cache
        cache[user_id] = cached_posts  # Update the cache with the new list

    return True  # Return True to indicate successful deletion

