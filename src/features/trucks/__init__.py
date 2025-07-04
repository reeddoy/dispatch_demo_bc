from fastapi import APIRouter
from ...shared.services.routers.utils import *
from .api_models import *
from .utils import *
from ...models import *


trucks_router = APIRouter(prefix="/trucks", tags=["Trucks"])


@trucks_router.get(
    "/",
    name="Get trucks of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": TrucksResponse,
            "description": "Trucks returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def trucks(
    page: int = 1,
    limit: int = 10,
    session: Session = get_session,
) -> TrucksResponse:
    if page < 1:
        page = 1
    pages = Trucks.count_pages(
        limit,
        dict(user_id=session.user.id),
    )
    trucks_ = Trucks.find(
        dict(user_id=session.user.id),
        limit=limit,
        skip=(page - 1) * limit,
        sort="created_timestamp",
        descending=True,
    )
    return TrucksResponse(
        trucks=[truck.dict for truck in trucks_],
        detail="Trucks returned successfully.",
        pages=pages,
        page=page,
    )


@trucks_router.get(
    "/saved",
    name="Get trucks of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": TrucksResponse,
            "description": "Saved trucks returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def saved(session: Session = get_session) -> TrucksResponse:
    user = session.user
    trucks_ids = user.saved_trucks

    trucks_: list[Truck] = []

    for l_id in trucks_ids:
        if truck := Trucks.get_child(l_id):
            trucks_.append(truck)

    return TrucksResponse(
        trucks=[truck.dict for truck in trucks_],
        detail="Saved trucks returned successfully.",
    )


@trucks_router.get(
    "/truck",
    name="Get a truck by its id.",
    responses={
        HTTP_200_OK: {
            "model": TruckResponse,
            "description": "Truck returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid truck_id.",
        },
    },
)
async def truck(truck_id: str, session: Session = get_session) -> TruckResponse:
    truck = Trucks.get_child(truck_id)
    if truck:
        return TruckResponse(
            truck=truck.dict,
            detail="Truck returned successfully.",
        )
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid truck_id")


@trucks_router.patch(
    "/truck",
    name="Update a truck data by its id.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Truck updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid truck_id.",
        },
    },
)
async def truck(
    truck_id: str,
    request: NewTruckRequest,
    session: Session = get_session,
) -> Response:
    truck: Truck = Trucks.get_child(truck_id)
    if truck:
        truck.update(**request.model_dump())
        return Response(detail="Truck updated successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid truck_id")


@trucks_router.get(
    "/all",
    name="Get all trucks.",
    responses={
        HTTP_200_OK: {
            "model": TrucksResponse,
            "description": "Trucks returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def all(session: Session = get_session) -> TrucksResponse:
    trucks_ = Trucks.find(sort="created_timestamp", descending=True)
    return TrucksResponse(
        trucks=[truck.dict for truck in trucks_],
        detail="Trucks returned successfully.",
    )


@trucks_router.post(
    "/search",
    name="Search trucks",
    responses={
        HTTP_200_OK: {
            "model": TrucksResponse,
            "description": "Trucks returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def search(
    request: SearchTruckRequest,
    _: Session = get_session,
) -> TrucksResponse:
    trucks_ = Trucks.find(
        sort="created_timestamp",
        descending=True,
    )

    trucks_ = filter_trucks(trucks_, request)

    return TrucksResponse(
        trucks=[truck.dict for truck in trucks_],
        detail="Trucks returned successfully.",
    )


@trucks_router.post(
    "/",
    name="Add a new truck",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Truck added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def trucks(
    request: NewTruckRequest,
    session: Session = get_session,
) -> Response:
    if Trucks.create(
        user_id=session.user.id,
        **request.model_dump(),
    ):
        return Response(detail="Truck added successfully.")
    else:
        raise HTTPException(
            HTTP_503_SERVICE_UNAVAILABLE,
            "Database error, try again later.",
        )


@trucks_router.post(
    "/save",
    name="Save a Truck",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Truck saved successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Truck with {id} does not exists.",
        },
    },
)
async def save(
    truck_id: str,
    session: Session = get_session,
) -> Response:
    user = session.user
    if Trucks.exists(truck_id):
        if truck_id not in user.saved_trucks:
            user.saved_trucks.append(truck_id)
            user.save()
        return Response(detail="Truck added successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Truck with {truck_id} does not exists.",
        )


@trucks_router.delete(
    "/unsave",
    name="Unsave a Truck",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Truck removed successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Truck with {id} does not exists.",
        },
    },
)
async def unsave(
    truck_id: str,
    session: Session = get_session,
) -> Response:
    user = session.user
    if Trucks.exists(truck_id):
        if truck_id in user.saved_trucks:
            user.saved_trucks.remove(truck_id)
            user.save()
        return Response(detail="Truck removed successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Truck with {truck_id} does not exists.",
        )


@trucks_router.delete(
    "/{id}",
    name="Delete a truck.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Truck deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def delete_truck(
    id: str,
    session: Session = get_session,
) -> Response:
    truck: Truck
    if truck := Trucks.get_child(id):
        Trucks.delete_child(truck._id)

        return Response(detail="Truck deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, truck does not exists.",
        )
