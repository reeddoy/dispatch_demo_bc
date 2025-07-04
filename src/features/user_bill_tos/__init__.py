from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ...models import *
from .utils import *


user_bill_tos_router = APIRouter(prefix="/user_bill_tos", tags=["User's bill tos"])


@user_bill_tos_router.get(
    "/",
    name="Get all user's bill tos",
    responses={
        HTTP_200_OK: {
            "model": UserBillTosResponse,
            "description": "User's bill tos returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_bill_tos(session: Session = get_session) -> UserBillTosResponse:
    user_bill_tos: list[UserBillTo] = UserBillTos.find(dict(user_id=session.user.id))
    return UserBillTosResponse(
        detail="User's bill tos returned successfully.",
        user_bill_tos=[
            UserBillToModel(
                id=user_bill_to.id,
                user_id=user_bill_to.user_id,
                company_name=user_bill_to.company_name,
                address=user_bill_to.address,
                phone_number=user_bill_to.phone_number,
                email=user_bill_to.email,
                notes=user_bill_to.notes,
            )
            for user_bill_to in user_bill_tos
        ],
    )


@user_bill_tos_router.get(
    "/{id}",
    name="Get a user's bill to",
    responses={
        HTTP_200_OK: {
            "model": UserBillToResponse,
            "description": "User's Bill To returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's bill to does not exists.",
        },
    },
)
async def user_bill_to(id: str, _: Session = get_session) -> UserBillToResponse:
    user_bill_to: UserBillTo
    if user_bill_to := UserBillTos.get_child(id):
        return getUserBillToResponse(
            user_bill_to,
            detail="User's bill tos returned successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's bill to does not exists.",
        )


@user_bill_tos_router.post(
    "/",
    name="Add a new user's bill to",
    responses={
        HTTP_200_OK: {
            "model": UserBillToResponse,
            "description": "User's Bill To added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def user_bill_tos(
    request: NewUserBillToRequest,
    session: Session = get_session,
) -> UserBillToResponse:
    if user_bill_to := UserBillTos.create(
        user_id=session.user.id, **request.model_dump()
    ):
        return getUserBillToResponse(
            user_bill_to,
            detail="User's Bill To added successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's bill to does not exists.",
        )


@user_bill_tos_router.patch(
    "/{id}",
    name="Update a user's bill to",
    responses={
        HTTP_200_OK: {
            "model": UserBillToResponse,
            "description": "User's Bill To updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's bill to does not exists.",
        },
    },
)
async def user_bill_to(
    id: str,
    request: NewUserBillToRequest,
    _: Session = get_session,
) -> UserBillToResponse:
    user_bill_to: UserBillTo
    if user_bill_to := UserBillTos.get_child(id):
        user_bill_to.update(**request.model_dump())
        return getUserBillToResponse(
            user_bill_to,
            detail="User's bill tos updated successfully.",
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's bill to does not exists.",
        )


@user_bill_tos_router.delete(
    "/{id}",
    name="Delete a user's bill to",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User's Bill To deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid id, user's bill to does not exists.",
        },
    },
)
async def user_bill_to(id: str, _: Session = get_session) -> Response:
    user_bill_to: UserBillTo
    if user_bill_to := UserBillTos.get_child(id):
        UserBillTos.delete_child(user_bill_to._id)
        return Response(detail="User's bill to deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, user's bill to does not exists.",
        )
