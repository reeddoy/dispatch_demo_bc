from fastapi import APIRouter

from ....shared.services.routers.utils import *
from .api_models import *


posts_router = APIRouter(prefix="/posts", tags=["Admin"])


@posts_router.get(
    "/",
    name="Get all posts",
    responses={
        HTTP_200_OK: {
            "model": UserPostsResponse,
            "description": "Posts returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def posts(_: Session = get_session) -> UserPostsResponse:
    posts: list[Post] = Posts.find()
    p_ = []
    for post in posts:
        user_id = post.user_id
        user: User
        if user := Users.get_child(user_id):
            p_.append(
                UserPost(
                    user_id=user_id,
                    username=user.user_name,
                    name=f"{user.first_name} {user.last_name}",
                    membership=user.membership,
                    user_type=user.user_type,
                    post_date=post.created_timestamp,
                    post_type="Post",
                    content=post.content,
                )
            )

    return UserPostsResponse(
        detail="Users returned successfully.",
        posts=p_,
    )
