from fastapi import APIRouter

from ...shared.services.servers.utils import *
from ...shared.services.routers.utils import *
from .api_models import *


notifications_router = APIRouter(prefix="/notifications", tags=["Notifications"])


@notifications_router.get(
    "/",
    name="Get notifications of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": NotificationResponse,
            "description": "Notifications returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def notifications(session: Session = get_session) -> NotificationResponse:
    notifications: list[Notifications] = Notifications.find(
        dict(user_id=session.user.id),
        sort="created_timestamp",
        descending=True,
    )
    return NotificationResponse(
        notifications=[
            NotificationModel(
                id=notification.id,
                created_timestamp=notification.created_timestamp,
                user_id=notification.user_id,
                uid=notification.uid,
                uid2=notification.uid2,
                type=notification.type,
                username=notification.username,
                fetched=notification.fetched,
            )
            for notification in notifications
        ],
        detail="Notifications returned successfully.",
    )


@notifications_router.delete(
    "/{id}",
    name="Delete a notification.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Notification deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def delete_notification(
    id: str,
    session: Session = get_session,
) -> NotificationResponse:
    notification: Notification
    if notification := Notifications.get_child(id):
        Notifications.delete_child(notification._id)
        return Response(detail="Notification deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, notification does not exists.",
        )


@sio_server.event
async def notifications(sid: str, _=None):
    print("notifications", sid)

    if session := await get_ws_session(sid):
        notifications: list[dict] = [
            dict(
                id=notification.id,
                created_timestamp=notification.created_timestamp,
                user_id=notification.user_id,
                uid=notification.uid,
                uid2=notification.uid2,
                type=notification.type,
                username=notification.username,
                fetched=notification.fetched,
            )
            for notification in Notifications.find(
                dict(user_id=session.user.id),
                sort="created_timestamp",
                descending=True,
            )
        ]

        await session.emit(
            lambda sid: sio_server.emit(
                "notifications",
                notifications,
                to=sid,
            )
        )
    else:
        await sio_server.emit(
            "invalid_session",
            "Login first",
            to=sid,
        )


@sio_server.event
async def notification(sid: str, id: str):
    print("notification", sid)

    if session := await get_ws_session(sid):
        notification: Notification = Notifications.get_child(id)
        if notification:
            notification.fetched = not notification.fetched
            notification.save()

        await session.emit(
            lambda sid: notifications(sid),
        )
    else:
        await sio_server.emit(
            "invalid_session",
            "Login first",
            to=sid,
        )


@sio_server.event
async def notifications_read(sid: str, _=None):
    print("notifications_read", sid)

    if session := await get_ws_session(sid):
        Notifications.update_many(
            {"user_id": session.user.id},
            {"$set": {"fetched": True}},
        )

        await session.emit(
            lambda sid: notifications(sid),
        )
    else:
        await sio_server.emit(
            "invalid_session",
            "Login first",
            to=sid,
        )


@sio_server.event
async def notifications_unread(sid: str, _=None):
    print("notifications_unread", sid)

    if session := await get_ws_session(sid):
        Notifications.update_many(
            {"user_id": session.user.id},
            {"$set": {"fetched": False}},
        )

        await session.emit(
            lambda sid: notifications(sid),
        )
    else:
        await sio_server.emit(
            "invalid_session",
            "Login first",
            to=sid,
        )


@sio_server.event
async def delete_notification(sid: str, id: str):
    print("delete_notification", sid)

    notification: Notification
    if notification := Notifications.get_child(id):
        Notifications.delete_child(notification._id)


@sio_server.event
async def delete_notifications(sid: str, _=None):
    print("delete_notifications", sid)

    if session := await get_ws_session(sid):
        Notifications.delete_children(dict(user_id=session.user.id))
