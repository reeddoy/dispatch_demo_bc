from fastapi import APIRouter
from pydantic import Base64Encoder

from ...shared.services.routers.utils import *
from ...shared.services.storage import upload_file
from .api_models import *
from .utils import *


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "/",
    name="Get all users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Users returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def users(_: Session = get_session) -> UsersResponse:
    users = [user.dict for user in Users.find(dict(active=True))]

    return dict(
        detail="Users returned successfully.",
        users=users,
    )


@users_router.get(
    "/profile",
    name="Get user profile",
    responses={
        HTTP_200_OK: {
            "model": GetUserProfileResponse,
            "description": "User profile returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User not found.",
        },
    },
)
async def profile(id: str, _: Session = get_session) -> GetUserProfileResponse:
    user: User = Users.get_child(id)
    if user:
        return GetUserProfileResponse(
            detail="User profile returned successfully.",
            profile=user.dict,
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User not found.",
        )


@users_router.patch(
    "/update_profile",
    name="Update user profile",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User profile updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def update_profile(
    request: UpdateUserProfileRequest,
    session: Session = get_session,
) -> Response:
    user = session.user
    user.update(**request.model_dump())
    return dict(detail="User profile updated successfully.")


@users_router.patch(
    "/update_profile_image",
    name="Update user profile image",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User profile image updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def update_profile_image(
    request: UpdateUserProfileImageRequest,
    session: Session = get_session,
) -> Response:
    user = session.user
    user.update(
        image=upload_file(
            request.image.filename,
            Base64Encoder.decode(request.image.data.encode()),
        )
    )
    return dict(detail="User profile image updated successfully.")


@users_router.patch(
    "/update_password",
    name="Update user password",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User password updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Incorrect old password.",
        },
    },
)
async def update_password(
    request: UpdateUserPasswordRequest,
    session: Session = get_session,
) -> Response:
    if verify_hash(request.old_password, session.user.password):
        session.user.update(password=request.new_password)
        return Response(detail="User password updated successfully.")
    else:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail="Incorrect old password.")


@users_router.get(
    "/dispatchers_n_carriers",
    name="Get dispatch users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Dispatch users returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def dispatchers_n_carriers(
    _: Session = get_session,
) -> UsersResponse:
    # users: list[User] = filter(filter_not_owners, Users.find())
    users: list[User] = Users.find({"$ne": "owner"})

    return dict(
        detail="Dispatch and Carrier users returned successfully.",
        users=[user.dict for user in users],
    )


@users_router.get(
    "/dispatchers",
    name="Get dispatch users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Dispatch users returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def dispatchers(_: Session = get_session) -> UsersResponse:
    _dispatchers: list[User] = Users.find({"user_type": UserType.dispatcher.name})

    return dict(
        detail="Dispatch users returned successfully.",
        users=[user.dict for user in _dispatchers],
    )


@users_router.get(
    "/saved_loads",
    name="Get users saved loads ids",
    responses={
        HTTP_200_OK: {
            "model": SavedLoads,
            "description": "Saved loads ids returned successfully.",
        },
    },
)
async def saved_loads(session: Session = get_session) -> SavedLoads:
    return SavedLoads(
        detail="Saved loads ids returned successfully.",
        saved_loads=session.user.saved_loads,
    )


@users_router.get(
    "/saved_trucks",
    name="Get users saved trucks ids",
    responses={
        HTTP_200_OK: {
            "model": SavedTrucks,
            "description": "Saved trucks ids returned successfully.",
        },
    },
)
async def saved_trucks(session: Session = get_session) -> SavedTrucks:
    return SavedTrucks(
        detail="Saved trucks ids returned successfully.",
        saved_trucks=session.user.saved_trucks,
    )


@users_router.get(
    "/favourites",
    name="Get favourite dispatch users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Favourite dispatch users returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def favourites(session: Session = get_session) -> UsersResponse:
    f_dispatchers = session.user.favourites

    users = [Users.get_child(f_d) for f_d in f_dispatchers]
    _dispatchers: list[User] = filter(filter_not_owners, users)

    return dict(
        detail="Favourite dispatch users returned successfully.",
        users=[user.dict for user in _dispatchers],
    )


@users_router.post(
    "/remove_favourite",
    name="Remove favourite dispatch users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Favourite dispatch user removed successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def remove_favourite(user_id: str, session: Session = get_session) -> Response:
    user = session.user
    if user_id in user.favourites:
        user.favourites.remove(user_id)
        user.save()

    return dict(detail="Favourite dispatch user removed successfully.")


@users_router.post(
    "/save_user",
    name="Save a dispatch user to favourite",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Dispatch user saved successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def save_user(user_id: str, session: Session = get_session) -> Response:
    user = session.user
    if user_id not in user.favourites:
        user.favourites.append(user_id)
        user.save()

    return dict(detail="Dispatch user saved successfully.")


@users_router.get(
    "/owners",
    name="Get owner users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Owners returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def owners(_: Session = get_session) -> UsersResponse:
    _owner: list[User] = filter(filter_owners, Users.find())
    _owner: list[User] = Users.find({"user_type": UserType.owner.name})

    return dict(
        detail="Owner returned successfully.",
        users=[user.dict for user in _owner],
    )


@users_router.get(
    "/carriers",
    name="Get carrier users",
    responses={
        HTTP_200_OK: {
            "model": UsersResponse,
            "description": "Carriers returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def carriers(_: Session = get_session) -> UsersResponse:
    _dispatchers: list[User] = Users.find({"user_type": UserType.carrier.name})

    return dict(
        detail="Carriers returned successfully.",
        users=[user.dict for user in _dispatchers],
    )


@users_router.get(
    "/check_availability",
    name="Get username availability",
    responses={
        HTTP_200_OK: {
            "model": AvailabilityResponse,
            "description": "Username availability returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def check_availability(
    username: str = "",
    email: str = "",
    phone_number: str = "",
) -> AvailabilityResponse:
    users: list[User] = Users.find(dict(active=True))
    username_availability = True
    email_availability = True
    phone_number_availability = True

    for user in users:
        if username_availability and username == user.user_name:
            username_availability = False
        if email_availability and email == user.email:
            email_availability = False
        if phone_number_availability and phone_number == user.phone_number:
            phone_number_availability = False

    return AvailabilityResponse(
        detail="Username availability returned successfully.",
        username=username,
        username_availability=username_availability,
        email=email,
        email_availability=email_availability,
        phone_number=phone_number,
        phone_number_availability=phone_number_availability,
    )


# @users_router.post(
#     "/delete_users",
#     name="Delete all users",
#     responses={
#         HTTP_200_OK: {
#             "model": Response,
#             "description": "Users deleted successfully.",
#         },
#         HTTP_404_NOT_FOUND: {
#             "model": Response,
#             "description": "Invalid unique_id.",
#         },
#     },
# )
# def delete_users(request: DeleteUserRequest):
#     if request.unique_id == "natty":
#         Users.delete_users()
#         return dict(message="Users deleted successfully.")

#     else:
#         raise HTTPException(
#             status_code=HTTP_404_NOT_FOUND,
#             detail="Invalid unique_id.",
#         )
