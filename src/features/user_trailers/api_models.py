from ...shared.services.routers.api_models import *


class NewUserTrailerRequest(BaseModel):
    trailer_number: str
    year: str
    make: str
    model: str
    tag_number: str
    notes: str


class UserTrailerModel(NewUserTrailerRequest):
    id: str
    user_id: str


class UserTrailerResponse(Response):
    user_trailer: UserTrailerModel


class UserTrailersResponse(Response):
    user_trailers: list[UserTrailerModel]
