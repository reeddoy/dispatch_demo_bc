import stripe
from fastapi import APIRouter
import stripe.error
from ....shared.services.routers.utils import *
from ....models import *
from .api_models import *


coupons_router = APIRouter(prefix="/coupons", tags=["Coupons"])


@coupons_router.get(
    "/",
    name="Get coupons.",
    responses={
        HTTP_200_OK: {
            "model": CouponsResponse,
            "description": "Coupons returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def coupons(session: Session = get_session) -> CouponsResponse:
    try:
        coupons = stripe.Coupon.list()
        return CouponsResponse(
            detail="Coupons fetched successfully",
            coupons=[
                CouponModel(
                    id=coupon.id,
                    amount_off=coupon.amount_off,
                    currency=coupon.currency,
                    duration=CouponDuration[coupon.duration],
                    duration_in_months=coupon.duration_in_months,
                    percent_off=coupon.percent_off,
                    name=coupon.name,
                    max_redemptions=coupon.max_redemptions,
                    created=coupon.created,
                    metadata=coupon.metadata,
                    redeem_by=coupon.redeem_by,
                    times_redeemed=coupon.times_redeemed,
                    valid=coupon.valid,
                )
                for coupon in coupons.data
            ],
        )
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@coupons_router.post(
    "/",
    name="Add a new coupon",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Coupon added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Response,
            "description": "Failed to create coupon",
        },
    },
)
async def coupons(request: CreateCoupon, session: Session = get_session) -> Response:
    try:
        percent_off = request.percent_off

        if request.amount_off and percent_off:
            percent_off = None

        coupon = stripe.Coupon.create(
            id=request.id,
            amount_off=request.amount_off or None,
            currency=request.currency or None,
            duration=request.duration.name or None,
            duration_in_months=request.duration_in_months or None,
            percent_off=percent_off,
            name=request.name,
            max_redemptions=request.max_redemptions or None,
        )

        stripe.PromotionCode.create(
            coupon=coupon.id,
            code=coupon.name,
        )

        return Response(detail="Coupon added successfully.")
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@coupons_router.delete(
    "/",
    name="Delete coupon.",
    responses={
        HTTP_200_OK: {
            "model": CouponsResponse,
            "description": "Coupon deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid coupon_id.",
        },
    },
)
async def coupon(coupon_id: str, session: Session = get_session) -> Response:
    try:
        stripe.Coupon.delete(coupon_id)
        return Response(detail="Coupon deleted successfully.")

    except:
        return HTTPException(HTTP_404_NOT_FOUND, detail="Invalid coupon_id")


# @coupons_router.post(
#     "/search",
#     name="Search loads",
#     responses={
#         HTTP_200_OK: {
#             "model": SearchCouponModel,
#             "description": "Loads returned successfully.",
#         },
#         HTTP_401_UNAUTHORIZED: {
#             "model": Response,
#             "description": "Invalid token, login first.",
#         },
#     },
# )
# async def search_coupons(
#     request: SearchCouponModel,
#     session: Session = get_session,
# ) -> CouponsResponse:
#     # coupons = filter(lambda coupons: filter_coupon(coupons, request), Coupons.find())
#     coupons = Coupons.find(search_or=request.model_dump())
#     return dict(
#         coupons=[coupons.dict for coupons in coupons],
#         detail="Coupons returned successfully.",
#     )
