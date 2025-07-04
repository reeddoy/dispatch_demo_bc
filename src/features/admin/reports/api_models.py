from ....shared.services.routers.api_models import *


class ReportModel(BaseModel):
    reporter: str
    reporter_id: str
    reporter_company_name: str
    report: str
    id: str
    reported: str
    reported_id: str
    created_timestamp: int
    files: list[str]


class ReportsResponse(Response):
    reports: list[ReportModel]
