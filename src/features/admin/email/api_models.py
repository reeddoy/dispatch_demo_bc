from typing import Optional
from ....shared.services.routers.api_models import *


class EmailRequest(BaseModel):
    email: str
    name: Optional[str] = ""
    subject: str
    body: str
    attachments: Optional[list[Media]] = None
