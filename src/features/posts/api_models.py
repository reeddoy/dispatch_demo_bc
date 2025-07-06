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



# New user info model for embedding user details
class UserInfoModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    user_name: str
    email: str

# Comment model with user info
class CommentWithUserModel(BaseModel):
    id: str
    content: str
    user: Optional[UserInfoModel]
    created_timestamp: int
    files: list[str] = []

# Updated PostModel with author, likes, and comments as user info
class PostModel(BaseModel):
    content: str
    id: str
    created_timestamp: int
    author: Optional[UserInfoModel]
    likes: list[UserInfoModel] = []
    comments: list[CommentWithUserModel] = []
    files: list[str] = []



class PostsResponse(Response):
    posts: list[PostModel]
    pages: Optional[int] = 0
    page: Optional[int] = 0



class PostResponse(Response):
    post: PostModel


class LikesResponse(Response):
    likes: list[str]
