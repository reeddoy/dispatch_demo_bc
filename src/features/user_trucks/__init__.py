from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_trucks_router = APIRouter(prefix="/user_trucks", tags=["User's trucks"])


@user_trucks_router.get(
    "/",
    name="Get all user's trucks",
    responses={
        HTTP_200_OK: {
            "model": UserTrucksResponse,
            "description": "User's trucks returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_trucks(session: Session = get_session) -> UserTrucksResponse:
    user_trucks: list[UserTruck] = UserTrucks.find(dict(user_id=session.user.id))
    return UserTrucksResponse(
        detail="User's trucks returned successfully.",
        user_trucks=[
            UserTruckModel(
                id=user_truck.id,
                user_id=user_truck.user_id,
                truck_number=user_truck.truck_number,
                year=user_truck.year,
                make=user_truck.make,
                model=user_truck.model,
                tag_number=user_truck.tag_number,
                notes=user_truck.notes,
            )
            for user_truck in user_trucks
        ],
    )


@user_trucks_router.get(
    "/{id}",
    name="Get a user's truck",
    responses={
        HTTP_200_OK: {
            "model": UserTruckResponse,
            "description": "User's truck returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's truck does not exists.",
        },
    },
)
async def user_truck(id: str, _: Session = get_session) -> UserTruckResponse:
    user_truck: UserTruck
    if user_truck := UserTrucks.get_child(id):
        return getUserTruckResponse(
            user_truck,
            detail="User's trucks returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's truck does not exists.",
        )


@user_trucks_router.post(
    "/",
    name="Add a new user's truck",
    responses={
        HTTP_200_OK: {
            "model": UserTruckResponse,
            "description": "User's truck added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_trucks(
    request: NewUserTruckRequest,
    session: Session = get_session,
) -> UserTruckResponse:
    if user_truck := UserTrucks.create(user_id=session.user.id, **request.model_dump()):
        return getUserTruckResponse(
            user_truck,
            detail="User's truck added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's truck does not exists.",
        )


@user_trucks_router.patch(
    "/{id}",
    name="Update a user's truck",
    responses={
        HTTP_200_OK: {
            "model": UserTruckResponse,
            "description": "User's truck updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's truck does not exists.",
        },
    },
)
async def user_truck(
    id: str,
    request: NewUserTruckRequest,
    _: Session = get_session,
) -> UserTruckResponse:
    user_truck: UserTruck
    if user_truck := UserTrucks.get_child(id):
        user_truck.update(**request.model_dump())
        return getUserTruckResponse(
            user_truck,
            detail="User's trucks updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's truck does not exists.",
        )


@user_trucks_router.delete(
    "/{id}",
    name="Delete a user's truck",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's truck deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's truck does not exists.",
        },
    },
)
async def user_truck(id: str, _: Session = get_session) -> Response:
    user_truck: UserTruck
    if user_truck := UserTrucks.get_child(id):
        UserTrucks.delete_child(user_truck._id)
        return Response(detail="User's trucks deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's truck does not exists.",
        )
