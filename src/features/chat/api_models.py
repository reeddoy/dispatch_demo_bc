from typing import Optional
from ...shared.services.routers.utils import *


class ChatData(BaseModel):
    receiver_id: str
    message: Optional[str] = ""
    url: Optional[str] = ""

    files: Optional[list[Media]] = []


class ChatModel(ChatData):
    id: str
    created_timestamp: int
    sender_id: str


class ContactModel(BaseModel):
    id: str
    name: str
    image_url: str
    last_message: str
    last_message_datetime: int
    online: bool


class ContactsResponse(Response):
    contacts: list[ContactModel]


"""
ssh root@193.43.134.115

193.43.134.115

@Draxysmith21

"""
