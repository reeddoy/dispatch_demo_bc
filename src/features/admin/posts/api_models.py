from ....shared.services.routers.api_models import *


class UserPost(BaseModel):
    user_id: str
    username: str
    name: str
    membership: str
    user_type: str
    post_date: int
    post_type: str
    content: str


class UserPostsResponse(Response):
    posts: list[UserPost]
