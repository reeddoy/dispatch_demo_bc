from typing import Optional
from ...shared.services.routers.api_models import *


class NewLoadReferralRequest(BaseModel):
    pickup: str
    delivery: str
    length: float
    equipment_type: str
    weight: float
    full_or_partial: str
    origin: str
    destination: str
    number_of_stops: int
    phone_number: str
    comments: str
    rate_estimate: float
    points: int
    xchange_rate: float
    trip_miles: str

    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0


class LoadReferralModel(NewLoadReferralRequest):
    id: str
    user_id: str


class LoadReferralsResponse(Response):
    load_referrals: list[LoadReferralModel]
    pages: Optional[int] = 0
    page: Optional[int] = 0


class LoadReferralResponse(Response):
    load_referral: LoadReferralModel


class SearchLoadReferralRequest(BaseModel):
    pickup: Optional[str] = ""
    length: Optional[float] = 0.0
    equipment_type: Optional[str] = ""
    origin: Optional[str] = ""

    destination: Optional[str] = ""
    delivery: Optional[str] = ""
    weight: Optional[float] = 0.0
    full_or_partial: Optional[str] = ""
    trip_miles: Optional[str] = ""

    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0
