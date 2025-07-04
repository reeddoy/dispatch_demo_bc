from .model import *


class Chat(Model):
    def __init__(
        self,
        models: "Chats",
        *,
        sender_id: str,
        receiver_id: str,
        files: list[dict] = [],
        message: str = "",
        url: str = "",
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.files = files
        self.message = message
        self.url = url


class Chats(Models):
    model_class = Chat


Chats = Chats()
