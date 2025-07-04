from ...shared.services.routers.api_models import *


class NewUserBillToRequest(BaseModel):
    company_name: str
    address: str
    phone_number: str
    email: str
    notes: str


class UserBillToModel(NewUserBillToRequest):
    id: str
    user_id: str


class UserBillToResponse(Response):
    user_bill_to: UserBillToModel


class UserBillTosResponse(Response):
    user_bill_tos: list[UserBillToModel]
