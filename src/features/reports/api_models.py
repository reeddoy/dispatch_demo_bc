from ..auth import *


class ReportRequest(BaseModel):
    reported_company_id: str
    report: str
    files: Optional[list[Media]] = []


class ReportModel(ReportRequest):
    id: str
    files: list[str]
    user_id: str
    company_name: str


class ReportsResponse(Response):
    reports: list[ReportModel]
