from fastapi import APIRouter

from ....shared.services.routers.utils import *
from ....shared.services.mail import *
from .api_models import *


email_router = APIRouter(prefix="/email", tags=["Admin"])


@email_router.post(
    "/",
    name="Send email",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Email sent successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def email(request: EmailRequest, _: Session = get_session) -> Response:
    email = request.email
    name = request.name
    subject = request.subject
    body = request.body
    attachments = request.attachments
    # todo
    Mail.send_email(
        to_email=email,
        to_name=name,
        subject=subject,
        body=body,
        attachments=attachments,
        as_html=True,
    )
    return Response(detail="Email sent successfully.")
