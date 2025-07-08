from ..auth import *


class GetUserProfileResponse(Response):
    profile: ProfileNoPassword


class UsersResponse(Response):
    users: list[ProfileNoPassword]


class SavedLoads(Response):
    saved_loads: list[str]


class SavedTrucks(Response):
    saved_trucks: list[str]


class UpdateUserProfileImageRequest(BaseModel):
    image: Media


class UpdateUserPasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UpdateUserProfileRequest(BaseModel):
    # user_type: UserType = ''
    first_name: str = ""
    last_name: str = ""
    company_name: str = ""
    email: str = ""
    address: str = ""
    # password: str = ''
    phone_number: str = ""

    # sign 2
    user_name: str = ""
    website: str = ""
    service_areas: list[str] = []
    dispatche_fees: list[str] = []
    accept_new_authorities: bool = False

    # sign 3
    ein: str = ""
    # XX-XXXXXXX=None

    mc: str = ""
    dot: str = ""
    offered_services: list[str] = []
    equipment_types: list[str] = []

    # sign 4
    description: str = ""


class AvailabilityResponse(Response):
    username: str
    username_availability: bool
    email: str
    email_availability: bool
    phone_number: str
    phone_number_availability: bool
