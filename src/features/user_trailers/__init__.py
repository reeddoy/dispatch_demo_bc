from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_trailers_router = APIRouter(prefix="/user_trailers", tags=["User's trailers"])


@user_trailers_router.get(
    "/",
    name="Get all user's trailers",
    responses={
        HTTP_200_OK: {
            "model": UserTrailersResponse,
            "description": "User's trailers returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_trailers(session: Session = get_session) -> UserTrailersResponse:
    user_trailers: list[UserTrailer] = UserTrailers.find(dict(user_id=session.user.id))
    return UserTrailersResponse(
        detail="User's trailers returned successfully.",
        user_trailers=[
            UserTrailerModel(
                id=user_trailer.id,
                user_id=user_trailer.user_id,
                trailer_number=user_trailer.trailer_number,
                year=user_trailer.year,
                make=user_trailer.make,
                model=user_trailer.model,
                tag_number=user_trailer.tag_number,
                notes=user_trailer.notes,
            )
            for user_trailer in user_trailers
        ],
    )


@user_trailers_router.get(
    "/{id}",
    name="Get a user's trailer",
    responses={
        HTTP_200_OK: {
            "model": UserTrailerResponse,
            "description": "User's trailer returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's trailer does not exists.",
        },
    },
)
async def user_trailer(id: str, _: Session = get_session) -> UserTrailerResponse:
    user_trailer: UserTrailer
    if user_trailer := UserTrailers.get_child(id):
        return getUserTrailerResponse(
            user_trailer,
            detail="User's trailers returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's trailer does not exists.",
        )


@user_trailers_router.post(
    "/",
    name="Add a new user's trailer",
    responses={
        HTTP_200_OK: {
            "model": UserTrailerResponse,
            "description": "User's trailer added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_trailers(
    request: NewUserTrailerRequest,
    session: Session = get_session,
) -> UserTrailerResponse:
    if user_trailer := UserTrailers.create(
        user_id=session.user.id, **request.model_dump()
    ):
        return getUserTrailerResponse(
            user_trailer,
            detail="User's trailer added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's trailer does not exists.",
        )


@user_trailers_router.patch(
    "/{id}",
    name="Update a user's trailer",
    responses={
        HTTP_200_OK: {
            "model": UserTrailerResponse,
            "description": "User's trailer updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's trailer does not exists.",
        },
    },
)
async def user_trailer(
    id: str,
    request: NewUserTrailerRequest,
    _: Session = get_session,
) -> UserTrailerResponse:
    user_trailer: UserTrailer
    if user_trailer := UserTrailers.get_child(id):
        user_trailer.update(**request.model_dump())
        return getUserTrailerResponse(
            user_trailer,
            detail="User's trailers updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's trailer does not exists.",
        )


@user_trailers_router.delete(
    "/{id}",
    name="Delete a user's trailer",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's trailer deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's trailer does not exists.",
        },
    },
)
async def user_trailer(id: str, _: Session = get_session) -> Response:
    user_trailer: UserTrailer
    if user_trailer := UserTrailers.get_child(id):
        UserTrailers.delete_child(user_trailer._id)
        return Response(detail="User's trailers deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's trailer does not exists.",
        )
