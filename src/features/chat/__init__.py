import traceback
from typing import Annotated
from fastapi import APIRouter, File, Form, UploadFile
from pydantic import Base64Encoder

from ...models.chat import Chats
from ...shared.services.routers.utils import *
from ...shared.services.storage import upload_file
from ...shared.services.servers.utils import *
from .api_models import *

chats_router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


@chats_router.get(
    "/contacts",
    name="Contacts of a user.",
    responses={
        HTTP_200_OK: {
            "model": ContactsResponse,
            "description": "Contacts returned successfully.",
        },
    },
)
def contacts(session: Session = get_session):
    contacts = session.user.contacts or []

    last_message_contact = []
    no_last_message_contact = []

    user: User
    for contact in contacts:
        if user := Users.get_child(contact):
            search_or = [
                dict(
                    sender_id=session.user.id,
                    receiver_id=user.id,
                ),
                dict(
                    receiver_id=session.user.id,
                    sender_id=user.id,
                ),
            ]

            chats: list[Chat] = Chats.find(
                search_or=search_or,
                limit=1,
                sort="created_timestamp",
                descending=True,
            )

            last_message = chats[0].message if chats else ""
            last_message_datetime = chats[0].created_timestamp if chats else 0
            online = False

            user_session: Session
            if user_session := Sessions.get_by_user_id(user.id):
                online = user_session.online

            (
                last_message_contact
                if last_message_datetime
                else no_last_message_contact
            ).append(
                dict(
                    id=user.id,
                    name=f"{user.first_name} {user.last_name}",
                    image_url=user.image,
                    last_message=last_message,
                    last_message_datetime=last_message_datetime,
                    online=online,
                )
            )

    last_message_contact.sort(
        key=lambda c: c["last_message_datetime"],
        reverse=True,
    )

    return dict(
        detail="Contacts returned successfully.",
        contacts=[last_message_contact + no_last_message_contact],
    )


@sio_server.event
async def contacts(sid: str, _=None):
    LOGGER.info(f"contacts-event: {sid}")

    if session := await get_ws_session(sid):
        contacts = session.user.contacts or []

        last_message_contact = []
        no_last_message_contact = []

        user: User
        for contact in contacts:
            if user := Users.get_child(contact):
                search_or = [
                    dict(
                        sender_id=session.user.id,
                        receiver_id=user.id,
                    ),
                    dict(
                        receiver_id=session.user.id,
                        sender_id=user.id,
                    ),
                ]

                chats: list[Chat] = Chats.find(
                    search_or=search_or,
                    limit=1,
                    sort="created_timestamp",
                    descending=True,
                )

                last_message = chats[0].message if chats else ""
                last_message_datetime = chats[0].created_timestamp if chats else 0
                online = False

                user_session: Session
                if user_session := Sessions.get_by_user_id(user.id):
                    online = user_session.online

                (
                    last_message_contact
                    if last_message_datetime
                    else no_last_message_contact
                ).append(
                    dict(
                        id=user.id,
                        name=f"{user.first_name} {user.last_name}",
                        image_url=user.image,
                        last_message=last_message,
                        last_message_datetime=last_message_datetime,
                        online=online,
                    )
                )

        last_message_contact.sort(
            key=lambda c: c["last_message_datetime"],
            reverse=True,
        )

        LOGGER.info(
            f"total-contacts: {len(last_message_contact + no_last_message_contact)}"
        )

        return await sio_server.emit(
            "contacts",
            last_message_contact + no_last_message_contact,
            to=sid,
        )


@sio_server.event
async def contact(sid: str, id: str):
    LOGGER.info(f"contact-delete-event: {sid} {id}")

    if session := await get_ws_session(sid):
        contacts_ = session.user.contacts or []
        if id in contacts_:
            contacts_.remove(id)
            session.user.save()
        await contacts(sid)


@chats_router.post(
    "/",
    name="Add a new chat",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Chat added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def chat(
    receiver_id: Annotated[str, Form()],
    message: Annotated[str, Form()] = "",
    url: Annotated[str, Form()] = "",
    files: list[Annotated[UploadFile, File()]] = [],
    session: Session = get_session,
):
    LOGGER.info(f"chat post, hasFile={bool(files)}")

    if not (message or files or url):
        raise HTTPException(
            HTTP_400_BAD_REQUEST, "Invalid message, no message, or files or url."
        )

    LOGGER.info(session)

    if session.online:
        files_paths: list[Media] = []

        for file in files:
            file_url = upload_file(
                file.filename,
                await file.read(),
            )
            files_paths.append(
                Media(
                    filename=file.filename,
                    data=file_url,
                ).model_dump()
            )

        receiver_session: Session
        receiver: User

        LOGGER.info(f"        User is online: {session}")

        receiver_session = Sessions.get_by_user_id(receiver_id)
        receiver = (
            receiver_session.user if receiver_session else Users.get_child(receiver_id)
        )

        if receiver:
            LOGGER.info(f"        Receiver is valid: {receiver}")

            message: Chat = Chats.create(
                sender_id=session.user.id,
                receiver_id=receiver_id,
                message=message,
                url=url,
                files=files_paths,
            )

            receiver.contacts = receiver.contacts or []
            session.user.contacts = session.user.contacts or []

            if receiver.id not in session.user.contacts:
                session.user.contacts.append(receiver.id)
                session.user.save()

            if session.user.id not in receiver.contacts:
                receiver.contacts.append(session.user.id)
                receiver.save()

            await session.emit(
                lambda sid: sio_server.emit(
                    "chat",
                    message.dict,
                    to=sid,
                )
            )
            await session.emit(lambda sid: contacts(sid))

            s = ""

            # receiver is online
            if receiver_session and receiver_session.online:
                LOGGER.info(f"        Receiver is online: {receiver_session}")

                await receiver_session.emit(
                    lambda sid: sio_server.emit(
                        "chat",
                        message.dict,
                        to=sid,
                    )
                )
                await receiver_session.emit(lambda sid: contacts(sid))

                s = " and receiver"

            LOGGER.info(f"emitting chat to sender{s}\n\n\n\n\n")
            return dict(detail="Chat added successfully.")
        else:
            LOGGER.info("emitting wrong_receiver_id")
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                "Message's receiver_id is not a valid user.",
            )
    else:
        LOGGER.info("User is offline")
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, "User is offline.")


@sio_server.event
async def chat(sid: str, data: dict):
    LOGGER.info(f"chat event {sid=}, hasFile={bool(data.get('files'))}")
    datas = {}

    for k, v in data.items():
        if k == "files":
            h = []
            for file in v:
                h.append(
                    dict(
                        filename=file["filename"],
                        data=len(file["data"]),
                    )
                )
            v = h
        datas[k] = v
    LOGGER.info(datas)

    try:
        message_request = ChatData(**data)

        receiver_session: Session
        receiver: User

        if user_session := await get_ws_session(sid):
            LOGGER.info(f"        User is online: {user_session}")

            if not (
                message_request.message or message_request.files or message_request.url
            ):
                return await sio_server.emit(
                    "invalid_message",
                    dict(
                        detail="Invalid message.",
                        message=data,
                    ),
                    to=sid,
                )

            files_paths: list[Media] = []
            if message_request.files:
                try:
                    for file in message_request.files:
                        path = upload_file(
                            file.filename,
                            Base64Encoder.decode(file.data.encode()),
                        )
                        files_paths.append(
                            Media(
                                filename=file.filename,
                                data=path,
                            ).model_dump()
                        )
                except Exception as e:
                    LOGGER.info(e)
                    traceback.print_exc()
                    return await sio_server.emit(
                        "invalid_message",
                        dict(
                            detail="Bad data encoding, ensure the data is base64 encoded.",
                            message=data,
                        ),
                        to=sid,
                    )

            kwargs = message_request.model_dump()
            kwargs["files"] = files_paths

            receiver_session = Sessions.get_by_user_id(message_request.receiver_id)
            LOGGER.info(receiver_session)

            receiver = (
                receiver_session.user
                if receiver_session
                else Users.get_child(message_request.receiver_id)
            )

            if receiver:
                LOGGER.info(f"        Receiver is valid: {receiver}")

                message: Chat = Chats.create(sender_id=user_session.user.id, **kwargs)

                receiver.contacts = receiver.contacts or []
                user_session.user.contacts = user_session.user.contacts or []

                if receiver.id not in user_session.user.contacts:
                    user_session.user.contacts.append(receiver.id)
                    user_session.user.save()

                if user_session.user.id not in receiver.contacts:
                    receiver.contacts.append(user_session.user.id)
                    receiver.save()

                await user_session.emit(
                    lambda sid: sio_server.emit(
                        "chat",
                        message.dict,
                        to=sid,
                    )
                )
                await user_session.emit(lambda sid: contacts(sid))

                s = ""

                # receiver is online
                if receiver_session and receiver_session.online:
                    LOGGER.info(f"        Receiver is online: {receiver_session}")

                    await receiver_session.emit(
                        lambda sid: sio_server.emit(
                            "chat",
                            message.dict,
                            to=sid,
                        )
                    )
                    await receiver_session.emit(lambda sid: contacts(sid))

                    s = " and receiver"

                LOGGER.info(f"emitting chat to sender{s}\n\n\n\n\n")

            else:
                LOGGER.info("emitting wrong_receiver_id")
                return await sio_server.emit(
                    "wrong_receiver_id",
                    "Message's receiver_id is not a valid user.",
                    to=sid,
                )
        else:
            LOGGER.info("User is offline")
            return

    except Exception as e:
        await sio_server.emit(
            "invalid_message",
            dict(
                detail="Message is invalid",
                message=data,
            ),
            to=sid,
        )
        LOGGER.info(e)
        traceback.print_exc()


@sio_server.event
async def chat_history(sid: str, other_user_id: str):
    LOGGER.info(f"chat_history {sid=}, {other_user_id=} ")

    if session := await get_ws_session(sid):
        chats: list[Chat] = Chats.find(
            search_or=[
                dict(
                    sender_id=session.user.id,
                    receiver_id=other_user_id,
                ),
                dict(
                    receiver_id=session.user.id,
                    sender_id=other_user_id,
                ),
            ]
        )

        data = dict(
            user_id=session.user.id,
            other_user_id=other_user_id,
            chat_history=[
                dict(
                    id=chat.id,
                    created_timestamp=chat.created_timestamp,
                    sender_id=chat.sender_id,
                    receiver_id=chat.receiver_id,
                    message=chat.message,
                    files=chat.files,
                    url=chat.url,
                )
                for chat in chats
            ],
        )
        LOGGER.info("emitting chat_history back to user")
        await session.emit(
            lambda sid: sio_server.emit(
                "chat_history",
                data,
                to=sid,
            )
        )
    else:
        await sio_server.emit("invalid_session", "Login first", to=sid)


@sio_server.event
async def chat_delete(sid: str, id: str):
    LOGGER.info(f"chat_delete {sid=}, {id=} ")

    if session := await get_ws_session(sid):
        chat: Chat = Chats.get_one(id)
        if chat:
            Chats.delete_child(chat._id)

        LOGGER.info("emitting chat_delete back to user")
        await session.emit(
            lambda sid: sio_server.emit("chat_delete", id, to=sid),
        )
    else:
        await sio_server.emit("invalid_session", "Login first", to=sid)
