from .model import *


class Report(Model):
    def __init__(
        self,
        models: "Reports",
        *,
        user_id: str,
        company_name: float,
        reported_company_name: str,
        reported_company_id: str,
        report: str,
        files: list[str] = [],
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.company_name = company_name
        self.reported_company_name = reported_company_name
        self.reported_company_id = reported_company_id
        self.report = report
        self.files = files


class Reports(Models):
    model_class = Report


Reports = Reports()
