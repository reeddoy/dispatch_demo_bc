from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_receivers_router = APIRouter(prefix="/user_receivers", tags=["User's receivers"])


@user_receivers_router.get(
    "/",
    name="Get all user's receivers",
    responses={
        HTTP_200_OK: {
            "model": UserReceiversResponse,
            "description": "User's receivers returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_receivers(session: Session = get_session) -> UserReceiversResponse:
    user_receivers: list[UserReceiver] = UserReceivers.find(
        dict(user_id=session.user.id)
    )
    return UserReceiversResponse(
        detail="User's receivers returned successfully.",
        user_receivers=[
            UserReceiverModel(
                id=user_receiver.id,
                user_id=user_receiver.user_id,
                contact_person=user_receiver.contact_person,
                company_name=user_receiver.company_name,
                phone_number=user_receiver.phone_number,
                notes=user_receiver.notes,
            )
            for user_receiver in user_receivers
        ],
    )


@user_receivers_router.get(
    "/{id}",
    name="Get a user's receiver",
    responses={
        HTTP_200_OK: {
            "model": UserReceiverResponse,
            "description": "User's receiver returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's receiver does not exists.",
        },
    },
)
async def user_receiver(id: str, _: Session = get_session) -> UserReceiverResponse:
    user_receiver: UserReceiver
    if user_receiver := UserReceivers.get_child(id):
        return getUserReceiverResponse(
            user_receiver,
            detail="User's receivers returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's receiver does not exists.",
        )


@user_receivers_router.post(
    "/",
    name="Add a new user's receiver",
    responses={
        HTTP_200_OK: {
            "model": UserReceiverResponse,
            "description": "User's receiver added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_receivers(
    request: NewUserReceiverRequest,
    session: Session = get_session,
) -> UserReceiverResponse:
    if user_receiver := UserReceivers.create(
        user_id=session.user.id, **request.model_dump()
    ):
        return getUserReceiverResponse(
            user_receiver,
            detail="User's receiver added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's receiver does not exists.",
        )


@user_receivers_router.patch(
    "/{id}",
    name="Update a user's receiver",
    responses={
        HTTP_200_OK: {
            "model": UserReceiverResponse,
            "description": "User's receiver updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's receiver does not exists.",
        },
    },
)
async def user_receiver(
    id: str,
    request: NewUserReceiverRequest,
    _: Session = get_session,
) -> UserReceiverResponse:
    user_receiver: UserReceiver
    if user_receiver := UserReceivers.get_child(id):
        user_receiver.update(**request.model_dump())
        return getUserReceiverResponse(
            user_receiver,
            detail="User's receivers updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's receiver does not exists.",
        )


@user_receivers_router.delete(
    "/{id}",
    name="Delete a user's receiver",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's receiver deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's receiver does not exists.",
        },
    },
)
async def user_receiver(id: str, _: Session = get_session) -> Response:
    user_receiver: UserReceiver
    if user_receiver := UserReceivers.get_child(id):
        UserReceivers.delete_child(user_receiver._id)
        return Response(detail="User's receivers deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's receiver does not exists.",
        )
