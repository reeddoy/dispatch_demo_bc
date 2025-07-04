from .model import *


class Comment(Model):
    def __init__(
        self,
        models: "Comments",
        *,
        user_id: str,
        post_id: str,
        content: str,
        files: list[str] = [],
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.files = files


class Comments(Models):
    model_class = Comment


Comments = Comments()
