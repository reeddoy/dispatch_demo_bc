from ....shared.services.routers.api_models import *


class Dispatchers(BaseModel):
    elite: int
    essential: int
    premium: int
    normal: int


class Owners(BaseModel):
    elite: int
    essential: int
    premium: int
    normal: int


class Carriers(BaseModel):
    elite: int
    essential: int
    premium: int
    normal: int


class Member(BaseModel):
    name: str
    value: int


class Membership(BaseModel):
    dispatchers: list[Member]
    owners: list[Member]
    carriers: list[Member]


class Value(Member):
    ...


class Dashboard(BaseModel):
    # all_users: int
    # active_users: int

    # all_loads: int
    # all_trucks: int
    # available_trucks: int
    # available_loads: int

    values: list[Value]
    membership: Membership


class DashboardResponse(Response):
    dashboard: Dashboard
