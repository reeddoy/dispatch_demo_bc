from typing import Optional
from ...shared.services.routers.api_models import *


# class NewCommentRequest(BaseModel):


class CommentModel(BaseModel):
    content: str
    post_id: str
    id: str
    user_id: str
    user_name: str
    created_timestamp: int
    files: list[str]


class CommentsResponse(Response):
    comments: list[CommentModel]
    pages: Optional[int] = 0
    page: Optional[int] = 0


# class NewPostRequest(BaseModel):


class PostModel(BaseModel):
    content: str
    id: str
    user_id: str
    likes: int
    comments: int
    created_timestamp: int
    files: list[str]


class PostsResponse(Response):
    posts: list[PostModel]
    pages: Optional[int] = 0
    page: Optional[int] = 0


class PostResponse(Response):
    post: PostModel


class LikesResponse(Response):
    likes: list[str]
