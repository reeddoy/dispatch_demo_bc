from ...models.chat import Chats
from ...shared.services.routers.utils import *
from ...shared.services.servers.utils import *
from ..notifications.api_models import NotificationType
from .api_models import *
from .lounges import Lounge, Lounges


async def _lounges(sid: str = None):
    LOGGER.info("Lounge::_lounges")

    await sio_server.emit(
        "lounges",
        dict(
            lounges=[l.details for l in Lounges.values()],
        ),
        to=sid,
    )

    LOGGER.info("Lounge::_lounges : ended")


async def _lounge_ended(skip_sid: str, room: str):
    LOGGER.info("Lounge::_lounge_ended")

    Lounges.delete_lounge(room)
    await sio_server.emit(
        "lounge_ended",
        skip_sid=skip_sid,
        room=room,
    )
    await sio_server.close_room(room)
    await _lounges()

    LOGGER.info("Lounge::_lounge_ended : ended")


@sio_server.event
async def lounges(sid: str):
    LOGGER.info("Lounge::lounges")

    await _lounges(sid)

    LOGGER.info("Lounge::lounges : ended")


@sio_server.event
async def end_lounge(sid: str):
    LOGGER.info("Lounge::end_lounge")

    if session := await get_ws_session(sid):
        if lounge := Lounges.get(session.user.id):
            await _lounge_ended(sid, lounge.id)

    LOGGER.info("Lounge::end_lounge : ended")


@sio_server.event
async def create_lounge(sid: str, lounge_title: str):
    LOGGER.info("Lounge::create_lounge")

    if session := await get_ws_session(sid):
        user = session.user
        lounge: Lounge = Lounges.create_lounge(user, sid, lounge_title)
        Notifications.create(
            user_id=user.id,
            uid=lounge.id,
            type=NotificationType.lounge,
        )

        await sio_server.enter_room(sid, lounge.id)
        await _lounges()

    LOGGER.info("Lounge::create_lounge : ended")


@sio_server.event
async def join_lounge(sid: str, lounge_id: str):
    LOGGER.info("Lounge::join_lounge")

    if session := await get_ws_session(sid):
        user = session.user
        lounge: Lounge

        if lounge := Lounges.get(lounge_id):
            participants = []
            for user_sid, user_id in lounge.participants_sids.items():
                participants.append(
                    dict(
                        user_sid=user_sid,
                        user_id=user_id,
                    )
                )

            LOGGER.info(participants)

            await sio_server.enter_room(sid, lounge.id)
            await sio_server.emit(
                "participants",
                dict(participants=participants),
                to=sid,
            )
            lounge.add_participant(user, sid)

            await _lounges()

    LOGGER.info("Lounge::join_lounge : ended")


@sio_server.event
async def leave_lounge(sid: str):
    LOGGER.info("Lounge::leave_lounge")

    lounge: Lounge
    for lounge in Lounges.values():
        if lounge.remove_participant(sid):
            try:
                await sio_server.leave_room(sid, lounge.id)
            except:
                ...

            if sid == lounge.creator_sid:
                await _lounge_ended(sid, lounge.id)

            else:
                await sio_server.emit(
                    "left_lounge",
                    dict(sid=sid),
                    skip_sid=sid,
                    room=lounge.id,
                )
                await _lounges()
    LOGGER.info("Lounge::leave_lounge : ended")


@sio_server.event
async def sending_signal(sid: str, data: dict):
    LOGGER.info("Lounge::sending_signal")

    user_sid = data.get("user_sid")
    signal = data.get("signal")
    lounge_id = data.get("lounge_id")
    lounge: Lounge

    if user_sid and signal and (lounge := Lounges.get(lounge_id)):
        await sio_server.emit(
            "user_joined",
            dict(
                signal=signal,
                sid=sid,
                caller_id=lounge.participants_sids[sid],
            ),
            to=user_sid,
            room=lounge.id,
        )

    LOGGER.info("Lounge::sending_signal : ended")


@sio_server.event
async def returning_signal(sid: str, data: dict):
    LOGGER.info("Lounge::returning_signal")

    caller_sid = data.get("caller_sid")
    signal = data.get("signal")
    lounge_id = data.get("lounge_id")

    await sio_server.emit(
        "received_returning_signal",
        dict(
            signal=signal,
            sid=sid,
        ),
        to=caller_sid,
        room=lounge_id,
    )

    LOGGER.info("Lounge::returning_signal : ended")
