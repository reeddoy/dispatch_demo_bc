from .model import *


class Post(Model):
    def __init__(
        self,
        models: "Posts",
        *,
        user_id: str,
        content: str,
        likes: list[str] = [],
        comments_ids: list[str] = [],
        files: list[str] = [],
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.content = content
        self.likes = likes
        self.comments_ids = comments_ids
        self.files = files


class Posts(Models):
    model_class = Post


Posts = Posts()
