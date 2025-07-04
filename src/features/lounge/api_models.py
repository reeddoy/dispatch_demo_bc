from ...shared.services.routers.utils import *


# class CreateLoungeEvent(BaseModel):
#     name: str
#     offer: dict


class LoungeEvent(BaseModel):
    lounge_id: str
    user_id: str


class CreateLounge(BaseModel):
    title: str
    description: str
    call_id: str


class LoungeModel(BaseModel):
    id: str
    title: str
    user_id: str
    description: str
    created: int
    active_time: int
    closed: bool
    participants: list[str]


class LoungeResponse(Response):
    id: str


class LoungesResponse(Response):
    lounges: list[LoungeModel]
