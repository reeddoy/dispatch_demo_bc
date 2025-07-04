from fastapi import APIRouter

from ....shared.services.routers.utils import *
from .api_models import *


reports_router = APIRouter(prefix="/reports", tags=["Admin"])


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
async def reports(_: Session = get_session) -> ReportsResponse:
    reports: list[Report] = Reports.find()
    reps = []
    for report in reports:
        reporter: User = Users.get_child(report.user_id)
        print(report.__dict__, reporter)
        if reporter:
            reps.append(
                ReportModel(
                    reporter=f"{reporter.first_name} {reporter.last_name}",
                    reporter_id=report.user_id,
                    reporter_company_name=report.company_name,
                    report=report.report,
                    id=report.id,
                    reported=report.reported_company_name,
                    reported_id=report.reported_company_id,
                    created_timestamp=report.created_timestamp,
                    files=report.files,
                )
            )

    return ReportsResponse(
        detail="Reports returned successfully.",
        reports=reps,
    )


@reports_router.get(
    "/user",
    name="Get reports on a user",
    responses={
        HTTP_200_OK: {
            "model": ReportsResponse,
            "description": "User reports returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User id does not exist.",
        },
    },
)
async def reports(
    user_id: str,
    _: Session = get_session,
) -> ReportsResponse:
    if Users.exists(user_id):
        reports: list[Report] = Reports.find(
            dict(
                reported_company_id=user_id,
            )
        )
        reps = []
        for report in reports:
            reporter: User = Users.get_child(report.user_id)

            reps.append(
                ReportModel(
                    reporter=f"{reporter.first_name} {reporter.last_name}",
                    reporter_id=report.user_id,
                    reporter_company_name=report.company_name,
                    report=report.report,
                    id=report.id,
                    reported=report.reported_company_name,
                    reported_id=report.reported_company_id,
                    created_timestamp=report.created_timestamp,
                    files=report.files,
                )
            )
        return ReportsResponse(
            detail="User reports returned successfully.",
            reports=reps,
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User id does not exist.",
        )


@reports_router.delete(
    "/{report_id}",
    name="Delete a report",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Report delete successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Report id does not exist.",
        },
    },
)
async def reports(
    report_id: str,
    _: Session = get_session,
) -> Response:
    if report := Reports.get_child(report_id):
        report: Report
        Reports.delete_child(report._id)
        return Response(detail="Report delete successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Report id does not exist.",
        )
