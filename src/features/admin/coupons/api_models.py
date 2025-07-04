from typing import Optional
from ....shared.services.routers.api_models import *


class CouponDuration(Enum):
    forever = "forever"
    once = "once"
    repeating = "repeating"


class CreateCoupon(BaseModel):
    id: Optional[str] = None
    amount_off: Optional[int] = None
    currency: Optional[str] = "USD"
    duration: CouponDuration
    duration_in_months: Optional[int] = None
    percent_off: Optional[int] = None
    name: str
    max_redemptions: Optional[int] = None


class CouponModel(CreateCoupon):
    created: int
    metadata: dict
    redeem_by: Optional[int] = None
    times_redeemed: int
    valid: bool


# class SearchCouponModel(BaseModel):
#     id: str = ""
#     name: str = ""
#     percent: int
#     expiry_date: int = 0
#     max_redemption_date: int = 0


class CouponsResponse(Response):
    coupons: list[CouponModel]
