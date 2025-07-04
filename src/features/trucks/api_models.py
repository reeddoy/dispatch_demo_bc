from typing import Optional
from ...shared.services.routers.api_models import *


class NewTruckRequest(BaseModel):
    pickup: str
    delivery: str
    full_or_partial: str
    weight: float
    origin: str
    destination: str
    available_point: int
    phone_number: str
    equipment_type: str
    length: float
    comments: str
    trip_miles: str

    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0


class TruckModel(NewTruckRequest):
    id: str
    user_id: str


class TrucksResponse(Response):
    trucks: list[TruckModel]
    pages: Optional[int] = 0
    page: Optional[int] = 0


class TruckResponse(Response):
    truck: TruckModel


class SearchTruckRequest(BaseModel):
    pickup: Optional[str] = ""
    length: Optional[float] = 0.0
    equipment_type: Optional[str] = ""
    origin: Optional[str] = ""
    available_point: Optional[int]
    destination: Optional[str] = ""
    delivery: Optional[str] = ""
    weight: Optional[float] = 0.0
    full_or_partial: Optional[str] = ""
    trip_miles: Optional[str] = ""

    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0
