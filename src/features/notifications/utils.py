from ...models import Notification
from ...shared.services.servers.utils import *


async def broadcastNotification(
    notification: Notification,
    skip: str = "",
):
    if skip:
        return await sio_server.emit(
            "notification",
            notification.dict,
            skip_sid=skip,
        )

    session: Session = Sessions.get_by_user_id(notification.user_id)

    if session and session.online:
        await session.emit(
            lambda sid: sio_server.emit(
                "notification",
                notification.dict,
                to=sid,
            )
        )
