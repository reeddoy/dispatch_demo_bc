from fastapi import APIRouter
from pydantic import Base64Encoder
from ...shared.services.routers.utils import *
from ...shared.services.storage import upload_file
from ...models import *
from .api_models import *


reports_router = APIRouter(prefix="/reports", tags=["Report"])


@reports_router.get(
    "/",
    name="Get all reports",
    responses={
        HTTP_200_OK: {
            "model": ReportsResponse,
            "description": "Reports returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def reports(session: Session = get_session) -> ReportsResponse:
    reports: list[Report] = Reports.find()
    return ReportsResponse(
        detail="Reports returned successfully.",
        reports=[
            ReportModel(
                id=report.id,
                user_id=report.user_id,
                company_name=report.company_name,
                reported_company_id=report.reported_company_id,
                report=report.report,
                files=report.files,
            )
            for report in reports
        ],
    )


@reports_router.get(
    "/{user_id}",
    name="Get all reports of a user",
    responses={
        HTTP_200_OK: {
            "model": ReportsResponse,
            "description": "Reports returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def reports(
    user_id: str,
    session: Session = get_session,
) -> ReportsResponse:
    reports: list[Report] = Reports.find(dict(user_id=user_id))
    return dict(
        detail="Reports returned successfully.",
        reports=[report.dict for report in reports],
    )


@reports_router.post(
    "/report",
    name="Post a report",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Report posted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Company does not exists.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "You can not report yourself.",
        },
    },
)
async def report(
    request: ReportRequest,
    session: Session = get_session,
) -> Response:
    files = []
    if request.files:
        try:
            for file in request.files:
                path = upload_file(
                    file.filename,
                    Base64Encoder.decode(file.data.encode()),
                )
                files.append(path)
        except:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail="Bad data encoding, ensure the data is base64 encoded.",
            )

    if request.reported_company_id == session.user.id:
        raise HTTPException(
            HTTP_406_NOT_ACCEPTABLE,
            detail="You can not report yourself.",
        )
    elif reported_company := Users.get_child(request.reported_company_id):
        reported_company: User
        Reports.create(
            user_id=session.user.id,
            company_name=session.user.company_name,
            reported_company_name=f"{reported_company.company_name}",
            reported_company_id=reported_company.id,
            report=request.report,
            files=files,
        )
        return dict(detail="Report posted successfully.")

    else:
        raise HTTPException(
            HTTP_406_NOT_ACCEPTABLE,
            detail="Company does not exists.",
        )


@reports_router.delete(
    "/report",
    name="Delete a report",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Report deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid report_id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def report(report_id: str, session: Session = get_session) -> Response:
    if report := Reports.get_child(report_id):
        Reports.delete_child(report._id)
        return dict(detail="Report deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            "Invalid report_id",
        )
