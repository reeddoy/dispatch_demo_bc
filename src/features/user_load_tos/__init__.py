from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_load_tos_router = APIRouter(prefix="/user_load_tos", tags=["User's load tos"])


@user_load_tos_router.get(
    "/",
    name="Get all user's load tos",
    responses={
        HTTP_200_OK: {
            "model": UserLoadTosResponse,
            "description": "User's load tos returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_load_tos(session: Session = get_session) -> UserLoadTosResponse:
    user_load_tos: list[UserLoadTo] = UserLoadTos.find(dict(user_id=session.user.id))
    return UserLoadTosResponse(
        detail="User's load tos returned successfully.",
        user_load_tos=[
            UserLoadToModel(
                id=user_load_to.id,
                user_id=user_load_to.user_id,
                company_name=user_load_to.company_name,
                address=user_load_to.address,
                phone_number=user_load_to.phone_number,
                email=user_load_to.email,
                notes=user_load_to.notes,
            )
            for user_load_to in user_load_tos
        ],
    )


@user_load_tos_router.get(
    "/{id}",
    name="Get a user's load to",
    responses={
        HTTP_200_OK: {
            "model": UserLoadToResponse,
            "description": "User's Load To returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's load to does not exists.",
        },
    },
)
async def user_load_to(id: str, _: Session = get_session) -> UserLoadToResponse:
    user_load_to: UserLoadTo
    if user_load_to := UserLoadTos.get_child(id):
        return getUserLoadToResponse(
            user_load_to,
            detail="User's load tos returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's load to does not exists.",
        )


@user_load_tos_router.post(
    "/",
    name="Add a new user's load to",
    responses={
        HTTP_200_OK: {
            "model": UserLoadToResponse,
            "description": "User's Load To added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_load_tos(
    request: NewUserLoadToRequest,
    session: Session = get_session,
) -> UserLoadToResponse:
    if user_load_to := UserLoadTos.create(
        user_id=session.user.id, **request.model_dump()
    ):
        return getUserLoadToResponse(
            user_load_to,
            detail="User's Load To added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's load to does not exists.",
        )


@user_load_tos_router.patch(
    "/{id}",
    name="Update a user's load to",
    responses={
        HTTP_200_OK: {
            "model": UserLoadToResponse,
            "description": "User's Load To updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's load to does not exists.",
        },
    },
)
async def user_load_to(
    id: str,
    request: NewUserLoadToRequest,
    _: Session = get_session,
) -> UserLoadToResponse:
    user_load_to: UserLoadTo
    if user_load_to := UserLoadTos.get_child(id):
        user_load_to.update(**request.model_dump())
        return getUserLoadToResponse(
            user_load_to,
            detail="User's load tos updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's load to does not exists.",
        )


@user_load_tos_router.delete(
    "/{id}",
    name="Delete a user's load to",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's Load To deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's load to does not exists.",
        },
    },
)
async def user_load_to(id: str, _: Session = get_session) -> Response:
    user_load_to: UserLoadTo
    if user_load_to := UserLoadTos.get_child(id):
        UserLoadTos.delete_child(user_load_to._id)
        return Response(detail="User's load tos deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's load to does not exists.",
        )
