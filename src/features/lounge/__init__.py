from fastapi import APIRouter
from ...models import Lounge, Lounges
from .api_models import *
from ..notifications.api_models import NotificationType, broadcastNotification


lounge_router = APIRouter(prefix="/lounge", tags=["Lounge"])


@lounge_router.get(
    "/",
    name="Get lounges.",
    responses={
        HTTP_200_OK: {
            "model": LoungesResponse,
            "description": "Lounges returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def lounges(session: Session = get_session) -> LoungesResponse:
    lounges_: list[Lounge] = Lounges.find(
        sort="created_timestamp",
        descending=True,
    )
    return LoungesResponse(
        lounges=[
            dict(
                id=lounge.id,
                title=lounge.title,
                user_id=lounge.user_id,
                description=lounge.description,
                created=lounge.created_timestamp,
                closed=lounge.closed,
                active_time=lounge.active_time,
                participants=lounge.participants,
            )
            for lounge in lounges_
        ],
        detail="Lounges returned successfully.",
    )


@lounge_router.post(
    "/",
    name="Add lounge.",
    responses={
        HTTP_200_OK: {
            "model": LoungeResponse,
            "description": "Lounge added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def lounges(
    request: CreateLounge, session: Session = get_session
) -> LoungeResponse:
    lounge = Lounges.create(
        **request.model_dump(),
        user_id=session.user.id,
        participants=[session.user.user_name],
    )

    notification = Notifications.create(
        user_id=session.user.id,
        # user_id="lounge_created",
        uid=lounge.id,
        uid2=lounge.call_id,
        type=NotificationType.lounge,
        username=session.user.user_name,
    )

    await session.emit(lambda sid: broadcastNotification(notification, sid))

    return LoungeResponse(
        detail="Lounges created successfully.",
        id=lounge.id,
    )


@lounge_router.post(
    "/join",
    name="Join a lounge.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Lounge joined successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Lounge not found.",
        },
    },
)
async def lounges(lounge_id: str, session: Session = get_session) -> Response:
    lounge: Lounge = Lounges.get_child(lounge_id.strip())
    if lounge:
        lounge.participants.append(session.user.user_name)
        lounge.participants = list(set(lounge.participants))
        lounge.save()

        return Response(detail="Lounges joined successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Lounge not found.")


@lounge_router.post(
    "/invite",
    name="Invite a user to a lounge.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "User invited successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User or lounge not found.",
        },
    },
)
async def invite_to_lounge(
    request: LoungeEvent,
    session: Session = get_session,
) -> Response:
    user: User = Users.get_child(request.user_id)
    lounge: Lounge = Lounges.get_child(request.lounge_id)

    if not lounge:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Lounge not found.")

    elif user:
        notification = Notifications.create(
            user_id=user.id,
            uid=request.lounge_id,
            uid2=lounge.call_id,
            type=NotificationType.lounge_invite,
            username=session.user.user_name,
        )
        await broadcastNotification(notification)

        return Response(detail="User invited successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="User not found.")


@lounge_router.post(
    "/leave",
    name="Leave a lounge.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Lounge left successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Lounge not found.",
        },
    },
)
async def lounges(lounge_id: str, session: Session = get_session) -> Response:
    lounge: Lounge = Lounges.get_child(lounge_id)
    if lounge:
        if session.user.user_name in lounge.participants:
            lounge.participants.remove(session.user.user_name)
            lounge.save()
        return Response(detail="Lounges left successfully.")

    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Lounge not found.")


@lounge_router.delete(
    "/",
    name="Close a lounge.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Lounge closed successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Lounge not found.",
        },
    },
)
async def lounges(lounge_id: str, session: Session = get_session) -> Response:
    lounge: Lounge = Lounges.get_child(lounge_id.strip())
    if lounge != None:
        if session.user.id in lounge.user_id:
            lounge.active_time = get_timestamp() - lounge.created_timestamp
            lounge.closed = True
            lounge.save()
        return Response(detail="Lounges closed successfully.")

    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Lounge not found.")
