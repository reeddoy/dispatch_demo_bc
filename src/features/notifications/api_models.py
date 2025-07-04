from ...shared.services.routers.api_models import *
from .utils import broadcastNotification


class NotificationType(Enum):
    comment = "comment"  ##
    like = "like"  ##
    lounge = "lounge"  ##
    lounge_invite = "lounge_invite"  ##
    review = "review"  ##
    review_reply = "review_reply"  ##
    directory_add = "directory_add"
    load = "load"


class NotificationModel(BaseModel):
    id: str
    created_timestamp: int

    user_id: str
    uid: str
    uid2: str
    type: str
    username: str
    fetched: bool


class NotificationResponse(Response):
    notifications: list[NotificationModel]
