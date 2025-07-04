from ...shared.services.routers.api_models import *


class NewUserReceiverRequest(BaseModel):
    company_name: str
    phone_number: str
    contact_person: str
    notes: str


class UserReceiverModel(NewUserReceiverRequest):
    id: str
    user_id: str


class UserReceiverResponse(Response):
    user_receiver: UserReceiverModel


class UserReceiversResponse(Response):
    user_receivers: list[UserReceiverModel]
