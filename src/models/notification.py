from .model import *


class Notification(Model):
    def __init__(
        self,
        models: "Notifications",
        *,
        user_id: str = "",
        uid: str = "",
        type: str = "",
        username: str = "",
        fetched: bool = False,
        uid2: str = "",
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.uid = uid
        self.type = type
        self.username = username
        self.fetched = fetched
        self.uid2 = uid2


class Notifications(Models):
    model_class = Notification


Notifications = Notifications()
