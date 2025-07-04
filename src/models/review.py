from .model import *


class Review(Model):
    def __init__(
        self,
        models: "Reviews",
        *,
        user_id: str,
        rating: float,
        rater_id: str,
        review: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.rating = rating
        self.rater_id = rater_id
        self.review = review


class Reviews(Models):
    model_class = Review


Reviews = Reviews()
