from fastapi import APIRouter
from pydantic import Base64Encoder


from ...shared.services.storage import upload_file
from ...shared.services.routers.utils import *
from ..notifications.api_models import NotificationType, broadcastNotification
from .utils import *


loads_router = APIRouter(prefix="/loads", tags=["Loads"])


@loads_router.get(
    "/",
    name="Get loads of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": LoadsResponse,
            "description": "Loads returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def loads(
    page: int = 1,
    limit: int = 10,
    session: Session = get_session,
) -> LoadsResponse:
    if page < 1:
        page = 1
    pages = Loads.count_pages(
        limit,
        dict(user_id=session.user.id),
    )
    loads_: list[Load] = Loads.find(
        dict(user_id=session.user.id),
        limit=limit,
        skip=(page - 1) * limit,
        sort="created_timestamp",
        descending=True,
    )
    return LoadsResponse(
        loads=get_loads(loads_),
        pages=pages,
        page=page,
        detail="Loads returned successfully.",
    )


@loads_router.get(
    "/saved",
    name="Get loads of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": LoadsResponse,
            "description": "Saved loads returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def loads(session: Session = get_session) -> LoadsResponse:
    user = session.user
    loads_ids = user.saved_loads

    loads_: list[Load] = []

    for l_id in loads_ids:
        if load := Loads.get_child(l_id):
            loads_.append(load)

    return LoadsResponse(
        loads=get_loads(loads_), detail="Saved loads returned successfully."
    )


@loads_router.get(
    "/load",
    name="Get a load by its id.",
    responses={
        HTTP_200_OK: {
            "model": LoadResponse,
            "description": "Load returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid load_id.",
        },
    },
)
async def loads(load_id: str, session: Session = get_session) -> LoadResponse:
    load = Loads.get_child(load_id)
    if load:
        return LoadResponse(load=get_load(load), detail="Load returned successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid load_id")


@loads_router.patch(
    "/load",
    name="Update a load data by its id.",
    responses={
        HTTP_200_OK: {
            "model": LoadResponse,
            "description": "Load updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid load_id.",
        },
    },
)
async def load(
    load_id: str,
    request: PatchLoadRequest,
    session: Session = get_session,
) -> LoadResponse:
    load: Load = Loads.get_child(load_id)
    if load:
        load.update(**request.model_dump())
        return LoadResponse(detail="Load updated successfully.", load=get_load(load))
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid load_id")


@loads_router.get(
    "/all",
    name="Get all the loads.",
    responses={
        HTTP_200_OK: {
            "model": LoadsResponse,
            "description": "Loads returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def all_loads(session: Session = get_session) -> LoadsResponse:
    loads_: list[Load] = Loads.find(
        sort="created_timestamp",
        descending=True,
    )
    return LoadsResponse(loads=get_loads(loads_), detail="Loads returned successfully.")


@loads_router.post(
    "/",
    name="Add a new load",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Load added successfully.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Bad data encoding, ensure the data is base64 encoded.",
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
async def loads(
    request: NewLoadRequest,
    session: Session = get_session,
) -> Response:
    count = Loads.count_documents(dict(user_id=session.user.id))
    files_paths = []
    if request.files:
        try:
            for file in request.files:
                path = upload_file(
                    file.filename,
                    Base64Encoder.decode(file.data.encode()),
                )
                files_paths.append(path)
        except:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail="Bad data encoding, ensure the data is base64 encoded.",
            )

    kwargs = request.model_dump()
    kwargs["files"] = files_paths

    if load := Loads.create(
        user_id=session.user.id,
        load_id=count + 1,
        **kwargs,
    ):
        # todo

        notification = Notifications.create(
            user_id=session.user.id,
            uid=load.id,
            type=NotificationType.load,
            username=session.user.user_name,
        )

        await session.emit(lambda sid: broadcastNotification(notification, sid))

        # todo

        return dict(detail="Load added successfully.")
    else:
        raise HTTPException(
            HTTP_503_SERVICE_UNAVAILABLE,
            "Database error, try again later.",
        )


@loads_router.post(
    "/search",
    name="Search loads",
    responses={
        HTTP_200_OK: {
            "model": LoadsResponse,
            "description": "Loads returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def search_loads(
    request: SearchLoadRequest,
    session: Session = get_session,
) -> LoadsResponse:
    loads_ = Loads.find(
        dict(user_id=session.user.id),
        sort="created_timestamp",
        descending=True,
    )

    loads_ = filter_loads(loads_, request)

    return LoadsResponse(loads=get_loads(loads_), detail="Loads returned successfully.")


@loads_router.delete(
    "/delete",
    name="Delete a Load",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Load deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Load with {id} does not exists.",
        },
    },
)
async def delete(
    load_id: str,
    session: Session = get_session,
) -> Response:
    user = session.user
    load: Load
    if load := Loads.get_child(load_id):
        Loads.delete_child(load._id)
        return dict(detail="Load deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Load with {load_id} does not exists.",
        )
