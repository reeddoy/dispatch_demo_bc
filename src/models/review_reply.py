from .model import *


class ReviewReply(Model):
    def __init__(
        self,
        models: "ReviewReplies",
        *,
        user_id: str,
        review_id: str,
        rater_id: str,
        reply: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.review_id = review_id
        self.rater_id = rater_id
        self.reply = reply


class ReviewReplies(Models):
    model_class = ReviewReply


ReviewReplies = ReviewReplies()
