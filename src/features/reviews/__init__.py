from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ..reviews.api_models import *
from ...models import *
from ..notifications.api_models import NotificationType, broadcastNotification


reviews_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@reviews_router.get(
    "/",
    name="Get all reviews",
    responses={
        HTTP_200_OK: {
            "model": ReviewsResponse,
            "description": "Reviews returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def reviews(session: Session = get_session) -> ReviewsResponse:
    reviews: list[Review] = Reviews.find()
    return ReviewsResponse(
        detail="Reviews returned successfully.",
        reviews=[
            ReviewModel(
                id=review.id,
                rater_id=review.rater_id,
                rating=review.rating,
                user_id=review.user_id,
                review=review.review,
            )
            for review in reviews
        ],
    )


@reviews_router.get(
    "/{user_id}",
    name="Get all reviews",
    responses={
        HTTP_200_OK: {
            "model": ReviewsResponse,
            "description": "Reviews returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def reviews(
    user_id: str,
    session: Session = get_session,
) -> ReviewsResponse:
    reviews: list[Review] = Reviews.find(dict(user_id=user_id))
    return ReviewsResponse(
        detail="Reviews returned successfully.",
        reviews=[
            ReviewModel(
                id=review.id,
                rater_id=review.rater_id,
                rating=review.rating,
                user_id=review.user_id,
                review=review.review,
            )
            for review in reviews
        ],
    )


@reviews_router.post(
    "/",
    name="Post a review",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Review posted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Company does not exists.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "You can not review yourself.",
        },
    },
)
async def reviews(
    request: ReviewRequest,
    session: Session = get_session,
) -> Response:
    if request.user_id == session.user.id:
        raise HTTPException(
            HTTP_406_NOT_ACCEPTABLE,
            detail="You can not review yourself.",
        )
    elif Users.exists(request.user_id):
        review = Reviews.create(
            user_id=request.user_id,
            rating=request.rating,
            rater_id=session.user.id,
            review=request.review,
        )

        notification = Notifications.create(
            user_id=request.user_id,
            uid=session.user.id,
            uid2=review.id,
            type=NotificationType.review,
            username=session.user.user_name,
        )
        await broadcastNotification(notification)

        return Response(detail="Review posted successfully.")

    else:
        raise HTTPException(
            HTTP_406_NOT_ACCEPTABLE,
            detail="Company does not exists.",
        )


@reviews_router.post(
    "/reply",
    name="Reply a review",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Review replied successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Review does not exists.",
        },
    },
)
async def reply_review(
    request: ReplyReviewRequest,
    session: Session = get_session,
) -> Response:
    if review := Reviews.find_one(
        dict(
            user_id=session.user.id,
            id=request.review_id,
        )
    ):
        review: Review
        review_reply = ReviewReplies.create(
            user_id=session.user.id,
            review_id=request.review_id,
            rater_id=review.rater_id,
            reply=request.reply,
        )

        notification = Notifications.create(
            user_id=review.rater_id,
            uid=session.user.id,
            uid2=review_reply.id,
            type=NotificationType.review_reply,
            username=session.user.user_name,
        )

        await broadcastNotification(notification)

        return Response(detail="Review replied successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Review does not exists.",
        )


@reviews_router.delete(
    "/",
    name="Delete a review",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Review deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid review_id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def review(review_id: str, session: Session = get_session) -> Response:
    if review := Reviews.get_child(review_id):
        Reviews.delete_child(review._id)
        return Response(detail="Review deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            "Invalid review_id",
        )
