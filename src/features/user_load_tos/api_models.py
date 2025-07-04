from ...shared.services.routers.api_models import *


class NewUserLoadToRequest(BaseModel):
    company_name: str
    address: str
    phone_number: str
    email: str
    notes: str


class UserLoadToModel(NewUserLoadToRequest):
    id: str
    user_id: str


class UserLoadToResponse(Response):
    user_load_to: UserLoadToModel


class UserLoadTosResponse(Response):
    user_load_tos: list[UserLoadToModel]
