from ....shared.services.routers.api_models import *


class AdminUser(BaseModel):
    user_id: str
    user_name: str
    membership: str
    user_type: str
    email: str
    loads: int
    trucks: int
    active_time: int
    reports: int


class AdminUsersResponse(Response):
    users: list[AdminUser]
