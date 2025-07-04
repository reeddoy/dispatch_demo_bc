from fastapi import APIRouter
from ...shared.services.routers.utils import *
from ..payment.utils import checkStripeCustomer
from .rewardful import *

_rewardful = Rewardful()

affiliates_router = APIRouter(prefix="/affiliate", tags=["Affiliates"])


def get_error(affiliate_data):
    if error := affiliate_data.get("error", ""):
        error = " ".join(
            [
                error,
                *affiliate_data.get("details", []),
            ]
        )
        affiliate_data = None

    return error, affiliate_data


@affiliates_router.get(
    "/",
    name="Get affiliate details of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": AffiliateResponse,
            "description": "Affiliate data returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def affiliate(session: Session = get_session) -> AffiliateResponse:
    checkStripeCustomer(session.user)

    error, affiliate_data = "", None

    if session.user.affiliate_id:
        error, affiliate_data = get_error(
            _rewardful.affiliate(
                session.user.affiliate_id,
            )
        )

    else:
        error, affiliate_data = get_error(
            _rewardful.create_affiliate(
                first_name=session.user.first_name,
                last_name=session.user.last_name,
                email=session.user.email,
                stripe_customer_id=session.user.customer_id,
            )
        )

        if affiliate_data:
            session.user.affiliate_id = affiliate_data.id
            session.user.save()

    if affiliate_data:
        return AffiliateResponse(
            affiliate=Affiliate(**affiliate_data),
            detail="Affiliate data returned successfully.",
        )
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=error,
        )
