from ...shared.services.routers.api_models import *


class NewUserTruckRequest(BaseModel):
    truck_number: str
    year: str
    make: str
    model: str
    tag_number: str
    notes: str


class UserTruckModel(NewUserTruckRequest):
    id: str
    user_id: str


class UserTruckResponse(Response):
    user_truck: UserTruckModel


class UserTrucksResponse(Response):
    user_trucks: list[UserTruckModel]
