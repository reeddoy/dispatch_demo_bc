from fastapi import APIRouter

from ...shared.services.routers.utils import *
from .api_models import *
from ...models import *
from .utils import *


load_referrals_router = APIRouter(
    prefix="/load_referrals",
    tags=["Load Referrals"],
)


@load_referrals_router.get(
    "/",
    name="Get load referrals of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": LoadReferralsResponse,
            "description": "Load referrals returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def load_referrals(
    page: int = 1,
    limit: int = 10,
    session: Session = get_session,
) -> LoadReferralsResponse:
    if page < 1:
        page = 1
    pages = LoadReferrals.count_pages(
        limit,
        dict(user_id=session.user.id),
    )
    load_referrals_ = LoadReferrals.find(
        dict(user_id=session.user.id),
        limit=limit,
        skip=(page - 1) * limit,
        sort="created_timestamp",
        descending=True,
    )
    return LoadReferralsResponse(
        load_referrals=get_load_referrals(load_referrals_),
        pages=pages,
        page=page,
        detail="Load referrals returned successfully.",
    )


@load_referrals_router.get(
    "/saved",
    name="Get load_referrals of the logged in user.",
    responses={
        HTTP_200_OK: {
            "model": LoadReferralsResponse,
            "description": "Saved load_referrals returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def saved(session: Session = get_session) -> LoadReferralsResponse:
    user = session.user
    load_referrals_ids = user.saved_loads

    load_referrals_: list[LoadReferral] = []

    for l_id in load_referrals_ids:
        if load_referral := LoadReferrals.get_child(l_id):
            load_referrals_.append(load_referral)

    return LoadReferralsResponse(
        load_referrals=get_load_referrals(load_referrals_),
        detail="Saved load_referrals returned successfully.",
    )


@load_referrals_router.get(
    "/load_referral",
    name="Get a load by its id.",
    responses={
        HTTP_200_OK: {
            "model": LoadReferralResponse,
            "description": "Load returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid load_referral_id.",
        },
    },
)
async def load_referral(
    load_referral_id: str,
    session: Session = get_session,
) -> LoadReferralResponse:
    load_referral = LoadReferrals.get_child(load_referral_id)
    if load_referral:
        return LoadReferralResponse(
            load_referral=get_load_referral(load_referral),
            detail="Load referral returned successfully.",
        )
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid truck_id")


@load_referrals_router.patch(
    "/load_referral",
    name="Update a load data by its id.",
    responses={
        HTTP_200_OK: {
            "model": LoadReferralResponse,
            "description": "Load updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid load_referral_id.",
        },
    },
)
async def load_referral(
    load_referral_id: str,
    request: NewLoadReferralRequest,
    session: Session = get_session,
) -> LoadReferralResponse:
    load_referral: LoadReferral = LoadReferrals.get_child(load_referral_id)
    if load_referral:
        load_referral.update(**request.model_dump())
        return LoadReferralResponse(
            load_referral=get_load_referral(load_referral),
            detail="Load referral updated successfully.",
        )
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid load_referral_id")


@load_referrals_router.post(
    "/",
    name="Add a new load referral",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Load referral added successfully.",
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
async def load_referrals(
    request: NewLoadReferralRequest,
    session: Session = get_session,
) -> Response:
    if LoadReferrals.create(
        user_id=session.user.id,
        **request.model_dump(),
    ):
        return Response(detail="Load referral added successfully.")
    else:
        raise HTTPException(
            HTTP_503_SERVICE_UNAVAILABLE,
            "Database error, try again later.",
        )


@load_referrals_router.get(
    "/all",
    name="Get all load referrals.",
    responses={
        HTTP_200_OK: {
            "model": LoadReferralsResponse,
            "description": "Load referrals returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def load_referrals(session: Session = get_session) -> LoadReferralsResponse:
    load_referrals_ = LoadReferrals.find(
        sort="created_timestamp",
        descending=True,
    )
    return LoadReferralsResponse(
        load_referrals=get_load_referrals(load_referrals_),
        detail="Load referrals returned successfully.",
    )


@load_referrals_router.post(
    "/search",
    name="Search load referrals",
    responses={
        HTTP_200_OK: {
            "model": LoadReferralsResponse,
            "description": "Load referrals returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def search_load_referrals(
    request: SearchLoadReferralRequest,
    _: Session = get_session,
) -> LoadReferralsResponse:
    load_referrals_ = LoadReferrals.find(
        sort="created_timestamp",
        descending=True,
    )

    load_referrals_ = filter_load_referrals(load_referrals_, request)

    return LoadReferralsResponse(
        load_referrals=get_load_referrals(load_referrals_),
        detail="Load referrals returned successfully.",
    )


@load_referrals_router.post(
    "/save",
    name="Save a load referral",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Load referral saved successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Load referral with {id} does not exists.",
        },
    },
)
async def save(
    load_referral_id: str,
    session: Session = get_session,
) -> Response:
    user = session.user
    if LoadReferrals.exists(load_referral_id):
        if load_referral_id not in user.saved_loads:
            user.saved_loads.append(load_referral_id)
            user.save()
        return Response(detail="Load referral saved successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Load referral with {load_referral_id} does not exists.",
        )


@load_referrals_router.delete(
    "/unsave",
    name="Unsave a load referral",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Load referral removed successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Load referral with {id} does not exists.",
        },
    },
)
async def unsave(
    load_referral_id: str,
    session: Session = get_session,
) -> Response:
    user = session.user
    if LoadReferrals.exists(load_referral_id):
        if load_referral_id in user.saved_loads:
            user.saved_loads.remove(load_referral_id)
            user.save()
        return Response(detail="Load referral removed successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Load referral with {load_referral_id} does not exists.",
        )


@load_referrals_router.delete(
    "/{id}",
    name="Delete a load_referral.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Load referral deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def delete_load_referral(
    id: str,
    session: Session = get_session,
) -> Response:
    load_referral: LoadReferral
    if load_referral := LoadReferrals.get_child(id):
        LoadReferrals.delete_child(load_referral._id)
        return Response(detail="Load referral deleted successfully.")
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid id, load_referral does not exists.",
        )
