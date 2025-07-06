from typing import Optional
from ...shared.services.routers.api_models import *
from ...constants.enums import *
from ...shared.utils.base import Child


class AdminUser(Child):
    def __init__(self, email: str):
        super().__init__()

        self.email = email
        self.verified = True


class SessionResponse(Response):
    token: str
    refresh_token: str


class SignupRequest(BaseModel):
    # sign 1
    user_type: UserType
    first_name: str
    last_name: str
    company_name: str
    email: str
    address: str
    password: str
    phone_number: str

    # sign 2
    user_name: str
    website: str
    service_areas: list[str]
    dispatche_fees: list[str]
    accept_new_authorities: bool

    # sign 3
    ein: str  # XX-XXXXXXX
    mc: str
    dot: str
    offered_services: list[str]
    equipment_types: list[str]

    # sign 4
    description: str
    referral: Optional[str] = ""


class Profile(SignupRequest):
    verified: bool
    id: str
    created_timestamp: int
    saved_loads: list[str]
    saved_trucks: list[str]
    favourites: list[str]
    membership: str
    contacts: Optional[list]
    image: str
    subscription_on: bool


class ContinueSignupRequest(BaseModel):
    user_type: UserType
    first_name: str
    phone_number: str
    email: str
    company_name: str
    address: str
    password: str


class LoginResponse(SessionResponse):
    profile: Profile
    refresh_token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class OTPData(BaseModel):
    timeout: int = 0
    otp: int = 0


class OTPResponse(Response):
    data: OTPData


class VerifyOTPRequest(BaseModel):
    otp: int


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class VerifyResetOTPRequest(BaseModel):
    otp: int
    email: str


class ResetPasswordRequest(BaseModel):
    otp: int
    email: str
    password: str


class DeleteUserRequest(BaseModel):
    unique_id: str
