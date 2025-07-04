from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_shippers_router = APIRouter(prefix="/user_shippers", tags=["User's shippers"])


@user_shippers_router.get(
    "/",
    name="Get all user's shippers",
    responses={
        HTTP_200_OK: {
            "model": UserShippersResponse,
            "description": "User's shippers returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_shippers(session: Session = get_session) -> UserShippersResponse:
    user_shippers: list[UserShipper] = UserShippers.find(dict(user_id=session.user.id))
    return UserShippersResponse(
        detail="User's shippers returned successfully.",
        user_shippers=[
            UserShipperModel(
                id=user_shipper.id,
                user_id=user_shipper.user_id,
                contact_person=user_shipper.contact_person,
                company_name=user_shipper.company_name,
                phone_number=user_shipper.phone_number,
                notes=user_shipper.notes,
            )
            for user_shipper in user_shippers
        ],
    )


@user_shippers_router.get(
    "/{id}",
    name="Get a user's shipper",
    responses={
        HTTP_200_OK: {
            "model": UserShipperResponse,
            "description": "User's shipper returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's shipper does not exists.",
        },
    },
)
async def user_shipper(id: str, _: Session = get_session) -> UserShipperResponse:
    user_shipper: UserShipper
    if user_shipper := UserShippers.get_child(id):
        return getUserShipperResponse(
            user_shipper,
            detail="User's shippers returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's shipper does not exists.",
        )


@user_shippers_router.post(
    "/",
    name="Add a new user's shipper",
    responses={
        HTTP_200_OK: {
            "model": UserShipperResponse,
            "description": "User's shipper added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_shippers(
    request: NewUserShipperRequest,
    session: Session = get_session,
) -> UserShipperResponse:
    if user_shipper := UserShippers.create(
        user_id=session.user.id, **request.model_dump()
    ):
        return getUserShipperResponse(
            user_shipper,
            detail="User's shipper added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's shipper does not exists.",
        )


@user_shippers_router.patch(
    "/{id}",
    name="Update a user's shipper",
    responses={
        HTTP_200_OK: {
            "model": UserShipperResponse,
            "description": "User's shipper updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's shipper does not exists.",
        },
    },
)
async def user_shipper(
    id: str,
    request: NewUserShipperRequest,
    _: Session = get_session,
) -> UserShipperResponse:
    user_shipper: UserShipper
    if user_shipper := UserShippers.get_child(id):
        user_shipper.update(**request.model_dump())
        return getUserShipperResponse(
            user_shipper,
            detail="User's shippers updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's shipper does not exists.",
        )


@user_shippers_router.delete(
    "/{id}",
    name="Delete a user's shipper",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's shipper deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's shipper does not exists.",
        },
    },
)
async def user_shipper(id: str, _: Session = get_session) -> Response:
    user_shipper: UserShipper
    if user_shipper := UserShippers.get_child(id):
        UserShippers.delete_child(user_shipper._id)
        return Response(detail="User's shippers deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's shipper does not exists.",
        )
