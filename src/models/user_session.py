from .model import *


class UserSession(Model):
    def __init__(
        self,
        models: "UserSessions",
        *,
        user_id: str,
        logged_in: bool,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.logged_in = logged_in


class UserSessions(Models):
    model_class = UserSession


UserSessions = UserSessions()
