from .model import *


class Lounge(Model):
    def __init__(
        self,
        models: "Lounges",
        *,
        title: str,
        user_id: str,
        call_id: str,
        description: str = "",
        active_time: int = 0,
        closed: bool = False,
        participants: list[str] = [],
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.title = title
        self.user_id = user_id
        self.call_id = call_id
        self.description = description
        self.active_time = active_time
        self.closed = closed
        self.participants = participants


class Lounges(Models):
    model_class = Lounge


Lounges = Lounges()
