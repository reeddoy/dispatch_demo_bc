from socketio import AsyncServer, ASGIApp

from ....constants.config import FROM_NAME, LOGGER
from ..routers.utils import *


wildcard = ["*", "http://localhost:3000"]
wildcard = ["*"]


sio_server = AsyncServer(
    cors_allowed_origins=wildcard[0],
    async_mode="asgi",
    logger=True,
    # engineio_logger=True,
    allow_upgrades=False,
    transports=["websocket", "polling"],
    max_http_buffer_size=4 * 1024 * 1024 * 1024,  # 4 GB
    connection_state_recovery=True,
)

sio_app = ASGIApp(
    socketio_server=sio_server,
    socketio_path="ws",
)


@sio_server.event
async def connect(sid: str, environ: dict, auth: dict = ""):
    if isinstance(auth, dict):
        token = auth.get("token", "")
    else:
        token = auth

    if token:
        try:
            session: Session = token_from_payload(token)
            LOGGER.info(f"SocketIO connected: {session}\n\n")

            # if session.online:
            #     await session.emit(lambda sid:  sio_server.disconnect(sid))

            # else:
            Sessions.set_session_sid(sid, session)

            await session.emit(
                lambda sid: sio_server.emit(
                    "status",
                    data=dict(
                        id=session.user.id,
                        online=True,
                    ),
                    skip_sid=sid,
                )
            )
            return True

        except HTTPException as e:
            await sio_server.emit("invalid_token", dict(detail=e.detail), to=sid)
            await sio_server.disconnect(sid)
    else:
        await sio_server.emit("invalid_token", dict(detail="Provide a token"), to=sid)
        await sio_server.disconnect(sid)

    return False


@sio_server.event
async def disconnect(sid: str):
    session: Session
    if session := Sessions.remove_session_sid(sid):
        LOGGER.info(f"SocketIO disconnected: {session}\n\n")

        try:
            await sio_server.emit(
                "status",
                data=dict(
                    id=session.user.id,
                    online=False,
                ),
                skip_sid=sid,
            )
        except Exception as e:
            ...

        # await leave_lounge(sid)
