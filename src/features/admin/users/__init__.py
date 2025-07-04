from fastapi import APIRouter
import stripe
from ....shared.services.routers.utils import *
from .api_models import *


users_router = APIRouter(prefix="/users", tags=["Admin"])


@users_router.get(
    "/",
    name="Get all users",
    responses={
        HTTP_200_OK: {
            "model": AdminUsersResponse,
            "description": "Users returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def users(_: Session = get_session) -> AdminUsersResponse:
    users: list[User] = Users.find({"active": True})
    u_ = []
    for user in users:
        user_id = user.id
        loads = Loads.find(dict(user_id=user_id))
        trucks = Trucks.find(dict(user_id=user_id))
        reports = Reports.find(dict(reported_company_id=user_id))
        u_.append(
            AdminUser(
                user_id=user_id,
                user_name=user.user_name,
                membership=user.membership,
                user_type=user.user_type,
                email=user.email,
                active= True,
                loads=len(loads),
                trucks=len(trucks),
                active_time=0,
                reports=len(reports),
            )
        )

    return AdminUsersResponse(
        detail="Users returned successfully.",
        users=u_,
    )


@users_router.delete(
    "/",
    name="Deactivate user",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Users deactivated successfully.",
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
async def delete_user(user_id: str, _: Session = get_session) -> Response:
    if user := Users.get_child(user_id):
        user: User
        def get_stripe_customer(email: str):
            customers = stripe.Customer.list(email=email).data
            return customers[0] if customers else None
        customer = get_stripe_customer(user.email)
        if customer:
            stripe.Customer.delete(customer.id)
        user.delete()
        return Response(
            detail="Users deactivated successfully.",
        )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
