from fastapi import FastAPI
from contextlib import asynccontextmanager


from ....constants.config import LOGGER
from ....models import *
from ...utils.commons import hash_data, run_on_thread
from ...services.mail import Mail

from ..routers.utils import *
from .sio_server import *


def admin_users():
    admins = (("admin@xdispatch.com", "admin-pass"),)
    for email, password in admins:
        if not Users.child_exists("email", email):
            Users.create(
                email=email,
                password=password,
                user_type="admin",
                first_name="admin",
                last_name="admin",
                user_name=email.split("@")[0],
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_on_thread(Mail.restart)
    admin_users()
    run_on_thread(Sessions.clear_sessions)

    yield

    Sessions.kill()
    await sio_server.shutdown()


async def get_ws_session(sid: str) -> Session:
    session: Session
    if session := Sessions.sids.get(sid):
        return session
    else:
        await sio_server.emit(
            "invalid_session",
            "Login first",
            to=sid,
        )
