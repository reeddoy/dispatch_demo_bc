from fastapi import APIRouter

from ...constants.config import LOGGER
from ...models import User
from ...shared.utils.validators import Validator
from ...shared.utils.commons import hash_data, verify_hash
from ...shared.services.routers.utils import *
from ...shared.services.sessions import *
from .api_models import *


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/signup",
    name="Register Account",
    responses={
        HTTP_201_CREATED: {
            "model": LoginResponse,
            "description": "Signed Up successfully.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid entry.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "User with email or phone number already exists.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def signup(request: SignupRequest) -> LoginResponse:
    email = request.email
    phone_number = request.phone_number
    detail = (
        Validator.validate_phone_number(phone_number)
        or Validator.validate_email(email)
        or Validator.validate_password(request.password)
    )

    if detail:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail=detail)

    elif not (
        user := Users.find_one(
            {
                "$or": [
                    {"email": email},
                    {"phone_number": phone_number},
                    {"id": hash_data(email)},
                ],
                "$and": [{"active": True}]
            }
        )
    ):
        user = Users.create(
            id=hash_data(email),
            **request.model_dump(),
            active=True,
        )
        session: Session = Sessions.create_session(user)

        try:
            session.client.send_otp()
            user.otp = session.client.otp.otp
            user.save()
        except Exception as e:
            LOGGER.info("...>", e)

        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content=dict(
                detail=f"Account created successful. OTP has been sent to `{email}`",
                profile=session.user.dict,
                refresh_token=get_refresh_token(session.id, session.user.id),
                token=get_access_token(session.id, session.user.id),
            ),
        )

    # elif user:
    #     user.delete()
    #     raise HTTPException(
    #         HTTP_409_CONFLICT,
    #         detail="User is deleted.",
    #     )

    else:
        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="User with provided details already exists.",
        )


def login_response(session: Session) -> LoginResponse:
    return LoginResponse(
        detail="Signed In successfully.",
        refresh_token=get_refresh_token(session.id, session.user.id),
        token=get_access_token(session.id, session.user.id),
        profile=session.user.dict,
    )


@auth_router.post(
    "/login",
    name="Login",
    responses={
        HTTP_200_OK: {
            "model": LoginResponse,
            "description": "Signed In successfully.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User not found.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid entry.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "User already signed in.",
        },
    },
)
async def login(request: LoginRequest) -> LoginResponse:
    email = request.email
    detail = Validator.validate_email(email) or Validator.validate_password(
        request.password
    )

    if detail:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail=detail)

    else:
        session: Session = Sessions.get_by_email(email)
        user: User

        if session and verify_hash(request.password, session.user.password):
            return login_response(session)
            raise HTTPException(
                HTTP_409_CONFLICT,
                detail="User already logged in.",
            )

        elif user := Users.find_one({"email":email, "active": True}):
            if verify_hash(request.password, user.password):
                # user_session: UserSession
                # if user_session := UserSessions.get_child(user.id):
                #     if user_session.logged_in:
                #         raise HTTPException(
                #             HTTP_409_CONFLICT,
                #             detail="User already logged in.",
                #         )
                #     else:
                #         user_session.update(logged_in=True)
                # else:
                #     user_session = UserSessions.create(user_id=user.id, logged_in=True)

                return login_response(Sessions.create_session(user))

            else:
                raise HTTPException(
                    HTTP_404_NOT_FOUND,
                    detail="Invalid credentials.",
                )

        else:
            raise HTTPException(
                HTTP_404_NOT_FOUND,
                detail=f"User with email `{email}` does not exist.",
            )


@auth_router.delete(
    "/logout",
    name="Logout",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Logged out successfully.",
        },
    },
)
async def logout(session: Session = get_session) -> Response:
    Sessions.remove_child(session)
    user_session: UserSession
    if user_session := UserSessions.get_child(session.user.id):
        user_session.update(logged_in=False)
    else:
        user_session = UserSessions.create(user_id=session.user.id, logged_in=False)

    return Response(detail="Logged out successfully.")


@auth_router.post(
    "/refresh_token",
    name="Refresh Token",
    responses={
        HTTP_200_OK: {
            "model": SessionResponse,
            "description": "Access token returned successfully.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid refresh token.",
        },
    },
)
async def refresh_token(request: RefreshTokenRequest) -> SessionResponse:
    refresh_token = request.refresh_token
    detail = Validator.validate(refresh_token, "Refresh token")

    if detail:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail=detail)

    else:
        session = token_from_payload(refresh_token, is_refresh=True)
        return dict(
            detail="Access token returned successfully.",
            token=get_access_token(session.id, session.user.id),
            refresh_token=refresh_token,
        )


@auth_router.get(
    "/send_otp",
    name="Send OTP to User`s phone number",
    responses={
        HTTP_200_OK: {
            "model": OTPResponse,
            "description": "OTP sent to email successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "Email already verified",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": OTPResponse,
            "description": "OTP service unavailable.",
        },
    },
)
async def send_otp(session: Session = get_session) -> OTPResponse:
    user = session.user
    # user.verified = False
    if user.verified:
        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="User already verified.",
        )

    else:
        try:
            # try:
            # session.client.send_otp()
        # except Exception as e:
        #     LOGGER.info(e)
            session.client.send_otp()
            user.otp = session.client.otp.otp
            user.save()

            # session.client.otp.send_otp()
            # otp = session.client.otp
            # otp.generate()

            # session.user.otp = otp.otp
            # session.user.save()

            return dict(
                data=dict(
                    otp=user.otp,
                    # timeout=otp.timeout,
                ),
                detail="OTP returned.",
            )

        except Exception as e:
            LOGGER.debug(f"send_otp:: {e}")
            raise HTTPException(
                HTTP_503_SERVICE_UNAVAILABLE,
                detail="OTP service unavailable.",
            )


@auth_router.post(
    "/verify_otp",
    name="Verify User",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User verified successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid OTP code.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "Email already verified.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "No OTP code.",
        },
    },
)
async def verify_otp(
    request: VerifyOTPRequest,
    session: Session = get_session,
) -> Response:
    if session.client.verified:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User already verified.",
        )

    elif session.user.otp == request.otp:
        session.user.verified = True
        session.user.otp = 0
        session.user.save()

        return dict(detail="User verified successfully.")

    elif not session.user.otp:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No OTP code.",
        )
    else:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid OTP code.",
        )


@auth_router.post(
    "/change_password",
    name="Change Password",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Password reset successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid password entry.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "Invalid old password.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
def change_password(
    request: ChangePasswordRequest,
    session: Session = get_session,
) -> Response:
    detail = Validator.validate_password(
        request.old_password
    ) or Validator.validate_password(request.new_password)

    if detail:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail=detail)

    else:
        if verify_hash(request.old_password, session.user.password):
            session.user.update(password=request.new_password)
            return dict(
                detail="Password updated successfully.",
            )

        else:
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail="Incorrect old password.",
            )


@auth_router.post(
    "/forgot_password",
    name="Forgot Password",
    responses={
        HTTP_200_OK: {
            "model": OTPResponse,
            "description": "Password reset OTP has been sent to email",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User with email `{email}` does not exists.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid email.",
        },
        HTTP_409_CONFLICT: {
            "model": OTPResponse,
            "description": "OTP already sent.",
        },
        HTTP_425_TOO_EARLY: {
            "model": Response,
            "description": "OTP already sent to email.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "OTP Service is currently unavailable.",
        },
    },
)
def forgot_password(request: ForgotPasswordRequest) -> OTPResponse:
    email = request.email
    detail = Validator.validate_email(email)

    if detail:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail=detail)

    else:
        if reset_otp := Sessions.reset_otps.get(request.email):
            return dict(
                data=dict(
                    otp=reset_otp.otp,
                    # timeout=reset_otp.timeout,
                ),
                detail=f"Reset OTP already sent to email `{request.email}`",  # , wait for {reset_otp.timeout_formated}.",
            )

        else:
            reset_otp: ResetOTP = Sessions.set_reset_password(email)
            if reset_otp:
                reset_otp.generate()
                return dict(
                    data=dict(
                        otp=reset_otp.otp,
                        # timeout=reset_otp.timeout,
                    ),
                    detail=f"Reset OTP sent to `{email}`",
                )
            else:
                raise HTTPException(
                    HTTP_404_NOT_FOUND,
                    detail=f"User with email `{email}` does not exists.",
                )


@auth_router.post(
    "/verify_reset_otp",
    name="Verify Reset OTP",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Password Reset OTP verified successfully.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "No prior reset action for this email.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Provided OTP is incorrect.",
        },
        HTTP_408_REQUEST_TIMEOUT: {
            "model": Response,
            "description": "OTP code Timeout.",
        },
    },
)
def verify_reset_otp(request: VerifyResetOTPRequest) -> Response:
    if reset_otp := Sessions.reset_otps.get(request.email.lower()):
        reset_otp: ResetOTP
        if reset_otp.verify(request.otp):
            return dict(detail="Password Reset OTP verified successfully.")

        elif not reset_otp.valid:
            raise HTTPException(
                status_code=HTTP_408_REQUEST_TIMEOUT,
                detail="Reset OTP code Timeout.",
            )
        else:
            raise HTTPException(
                status_code=HTTP_406_NOT_ACCEPTABLE,
                detail="Provided OTP is incorrect.",
            )
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No prior reset action for this email.",
        )


@auth_router.post(
    "/reset_password",
    name="Reset Password",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Password reset successfully.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "No prior reset action for this email.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Provided OTP is incorrect.",
        },
    },
)
def reset_password(request: ResetPasswordRequest) -> Response:
    if request.email in Sessions.reset_otps:
        if Sessions.reset_password(request.email, request.password, request.otp):
            return dict(detail="Password reset successfully.")

        else:
            raise HTTPException(
                status_code=HTTP_406_NOT_ACCEPTABLE,
                detail="Provided OTP is incorrect.",
            )

    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No prior reset action for this email.",
        )


# @auth_router.post(
#     "/admin_login",
#     name="Amin Login",
#     responses={
#         HTTP_200_OK: {
#             "model": SessionResponse,
#             "description": "Admin logged in successfully.",
#         },
#         HTTP_404_NOT_FOUND: {
#             "model": Response,
#             "description": "Admin details error.",
#         },
#     },
# )
# def admin_login(request: LoginRequest) -> SessionResponse:
#     if request.email == "admin@xdispatch.com" and request.password == "admin-pass":
#         session: Session = Sessions.add_child(Session(AdminUser(request.email)))

#         return dict(
#             detail="Admin logged in successfully.",
#             refresh_token=get_refresh_token(session.id, session.user.id),
#             token=get_access_token(session.id, session.user.id),
#         )

#     else:
#         raise HTTPException(
#             status_code=HTTP_404_NOT_FOUND,
#             detail="Admin details are invalid.",
#         )
