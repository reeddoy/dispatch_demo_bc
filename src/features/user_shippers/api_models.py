from ...shared.services.routers.api_models import *


class NewUserShipperRequest(BaseModel):
    company_name: str
    phone_number: str
    contact_person: str
    notes: str


class UserShipperModel(NewUserShipperRequest):
    id: str
    user_id: str


class UserShipperResponse(Response):
    user_shipper: UserShipperModel


class UserShippersResponse(Response):
    user_shippers: list[UserShipperModel]
