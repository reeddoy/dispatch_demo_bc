from ...shared.services.routers.api_models import *


class NewUserDriverRequest(BaseModel):
    driver_name: str
    address: str
    phone_number: str
    email: str
    notes: str


class UserDriverModel(NewUserDriverRequest):
    id: str
    user_id: str


class UserDriverResponse(Response):
    user_driver: UserDriverModel


class UserDriversResponse(Response):
    user_drivers: list[UserDriverModel]
