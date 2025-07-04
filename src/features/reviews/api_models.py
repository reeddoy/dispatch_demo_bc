from ..auth import *


class ReviewRequest(BaseModel):
    user_id: str
    review: str
    rating: float


class ReplyReviewRequest(BaseModel):
    review_id: str
    reply: str


class ReviewModel(ReviewRequest):
    id: str
    rater_id: str


class ReviewsResponse(Response):
    reviews: list[ReviewModel]
