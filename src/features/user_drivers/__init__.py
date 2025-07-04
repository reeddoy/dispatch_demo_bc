from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_drivers_router = APIRouter(prefix="/user_drivers", tags=["User's drivers"])


@user_drivers_router.get(
    "/",
    name="Get all user's drivers",
    responses={
        HTTP_200_OK: {
            "model": UserDriversResponse,
            "description": "User's drivers returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_drivers(session: Session = get_session) -> UserDriversResponse:
    user_drivers: list[UserDriver] = UserDrivers.find(dict(user_id=session.user.id))
    return UserDriversResponse(
        detail="User's drivers returned successfully.",
        user_drivers=[
            UserDriverModel(
                id=user_driver.id,
                user_id=user_driver.user_id,
                driver_name=user_driver.driver_name,
                address=user_driver.address,
                phone_number=user_driver.phone_number,
                email=user_driver.email,
                notes=user_driver.notes,
            )
            for user_driver in user_drivers
        ],
    )


@user_drivers_router.get(
    "/{id}",
    name="Get a user's driver",
    responses={
        HTTP_200_OK: {
            "model": UserDriverResponse,
            "description": "User's driver returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's driver does not exists.",
        },
    },
)
async def user_driver(id: str, _: Session = get_session) -> UserDriverResponse:
    user_driver: UserDriver
    if user_driver := UserDrivers.get_child(id):
        return getUserDriverResponse(
            user_driver,
            detail="User's driver returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's driver does not exists.",
        )


@user_drivers_router.post(
    "/",
    name="Add a new user's driver",
    responses={
        HTTP_200_OK: {
            "model": UserDriverResponse,
            "description": "User's driver added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_drivers(
    request: NewUserDriverRequest,
    session: Session = get_session,
) -> UserDriverResponse:
    if user_driver := UserDrivers.create(
        user_id=session.user.id,
        **request.model_dump(),
    ):
        return getUserDriverResponse(
            user_driver,
            detail="User's driver added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's driver does not exists.",
        )


@user_drivers_router.patch(
    "/{id}",
    name="Update a user's driver",
    responses={
        HTTP_200_OK: {
            "model": UserDriverResponse,
            "description": "User's driver updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's driver does not exists.",
        },
    },
)
async def user_driver(
    id: str,
    request: NewUserDriverRequest,
    _: Session = get_session,
) -> UserDriverResponse:
    user_driver: UserDriver
    if user_driver := UserDrivers.get_child(id):
        user_driver.update(**request.model_dump())
        return getUserDriverResponse(
            user_driver,
            detail="User's drivers updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's driver does not exists.",
        )


@user_drivers_router.delete(
    "/{id}",
    name="Delete a user's driver",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's driver deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's driver does not exists.",
        },
    },
)
async def user_driver(id: str, _: Session = get_session) -> Response:
    user_driver: UserDriver
    if user_driver := UserDrivers.get_child(id):
        UserDrivers.delete_child(user_driver._id)
        return Response(detail="User's drivers deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's driver does not exists.",
        )
