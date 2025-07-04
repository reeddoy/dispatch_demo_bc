from collections import OrderedDict
import json
from fastapi import APIRouter, Header, Request

from ...constants.config import LOGGER

from ...models import *
from .utils import *


payment_router = APIRouter(prefix="/payments", tags=["Payment"])


@payment_router.get(
    "/prices",
    name="Get prices of packages.",
    responses={
        HTTP_200_OK: {
            "model": PricesResponse,
            "description": "Prices returned successfully.",
        },
    },
)
async def prices(
    session: Session = get_session,
) -> PricesResponse:
    prices = stripe.Price.list().data

    return PricesResponse(
        detail="Prices returned successfully.",
        prices=prices,
    )


@payment_router.get(
    "/packages",
    name="Get packages.",
    responses={
        HTTP_200_OK: {
            "model": PackagesResponse,
            "description": "Packages returned successfully.",
        },
    },
)
async def packages(
    session: Session = get_session,
) -> PackagesResponse:
    packages = stripe.Product.list().data

    return PackagesResponse(
        detail="Packages returned successfully.",
        packages=packages,
    )


@payment_router.post(
    "/subscribe_elite",
    name="Subscription to Elite package.",
    responses={
        HTTP_200_OK: {
            "model": CheckOutSessionResponse,
            "description": "Checkout Session id returned successfully.",
        },
    },
)
async def subscribe_elite(
    request: CheckOutSessionRequest,
    session: Session = get_session,
) -> CheckOutSessionResponse:
    return create_checkout_session(
        "Elite",
        request,
        session,
    )


@payment_router.post(
    "/subscribe_essential",
    name="Subscription to Essential package.",
    responses={
        HTTP_200_OK: {
            "model": CheckOutSessionResponse,
            "description": "Checkout Session id returned successfully.",
        },
    },
)
async def subscribe_essential(
    request: CheckOutSessionRequest,
    session: Session = get_session,
) -> CheckOutSessionResponse:
    return create_checkout_session(
        "Essential",
        request,
        session,
    )


@payment_router.post(
    "/subscribe_premium",
    name="Subscription to Premium package.",
    responses={
        HTTP_200_OK: {
            "model": CheckOutSessionResponse,
            "description": "Checkout Session id returned successfully.",
        },
    },
)
async def subscribe_premium(
    request: CheckOutSessionRequest,
    session: Session = get_session,
) -> CheckOutSessionResponse:
    return create_checkout_session(
        "Premium",
        request,
        session,
    )


@payment_router.post(
    "/create_portal_session",
    name="Get billing portal session url.",
    responses={
        HTTP_200_OK: {
            "model": PortalSessionResponse,
            "description": "Portal session url returned successfully.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Subcribe first.",
        },
    },
)
async def create_portal_session(
    request: PortalSessionRequest,
    session: Session = get_session,
) -> PortalSessionResponse:
    try:
        checkStripeCustomer(session.user)
        portal_session = stripe.billing_portal.Session.create(
            customer=session.user.customer_id,
            return_url=request.return_url,
        )
        return PortalSessionResponse(
            detail="Portal session url returned successfully.",
            session_url=portal_session.url,
        )
    except:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR)


@payment_router.post(
    "/resume_subscription",
    name="Resume user subscription.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Subscription resumed successfully.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User not found.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Not subscribed to any package.",
        },
    },
)
async def resume_subscription(user_id: str, session: Session = get_session) -> Response:
    if user := Users.get_child(user_id):
        user: User
        subscription: Subscription = Subscriptions.get_one(
            "customer_id", user.customer_id
        )
        if subscription:
            try:
                stripe.Subscription.resume(
                    subscription.subcription_id,
                    billing_cycle_anchor="now",
                )
                user.subscription_on = True

            except:
                user.membership = ""
                user.subscription_on = False

            user.save()
            return Response(
                detail="Subscription resumed successfully.",
            )

        else:
            user.membership = ""
            user.subscription_on = False

            user.save()
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail="Not subscribed to any package.",
            )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User not found.",
        )


@payment_router.post(
    "/pause_subscription",
    name="Cancel user subscription.",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Subscription paused successfully.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User not found.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Not subscribed to any package.",
        },
    },
)
async def pause_subscription(user_id: str, session: Session = get_session) -> Response:
    user: User
    if user := Users.get_child(user_id):
        subscription: Subscription = Subscriptions.get_one(
            "customer_id", user.customer_id
        )
        if subscription:
            try:
                stripe.Subscription.cancel(
                    subscription.subcription_id,
                    prorate=True,
                )
                user.subscription_on = False
            except:
                user.membership = ""
                user.subscription_on = False

            user.save()

            return Response(
                detail="Subscription cancelled successfully.",
            )
        else:
            user.membership = ""
            user.subscription_on = False

            user.save()
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail="Not subscribed to any package.",
            )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User not found.",
        )


@payment_router.post("/webhook", name="Receives Stripe webhooks.")
async def webhook(
    request: Request,
    stripe_signature: str = Header(None),
):
    event = None
    payload = await request.body()

    data = json.loads(payload, object_pairs_hook=OrderedDict)
    event = stripe.Event.construct_from(data, stripe.api_key)
    session = None

    if event["type"] == "checkout.session.completed":
        session: stripe.checkout.Session = event["data"]["object"]
        subscription = session.subscription
        package = session.metadata.get("package")
        user_id = session.metadata.get("user_id")

        session = Sessions.get_by_user_id(user_id)

        user: User = session.user if session else Users.get_child(user_id)

        if package and user and session.payment_status == "paid":
            subscription: Subscriptions = Subscriptions.create(
                subcription_id=subscription,
                customer=session.customer,
                user_id=user.id,
                package=package,
                currency=session.currency,
            )
            user.membership = package
            user.subscription_on = True
            user.save()

    elif event["type"] == "customer.subscription.created":
        subscription: stripe.Subscription = event["data"]["object"]

        if user := getUser(subscription.customer):
            product = stripe.Product.retrieve(subscription.plan.product)
            user.membership = product.name.split(" ")[0]
            user.subscription_on = True
            user.save()

    elif event["type"] == "customer.subscription.deleted":
        subscription: stripe.Subscription = event["data"]["object"]

        if user := getUser(subscription.customer):
            user.membership = ""
            user.subscription_on = False
            user.save()

    elif event["type"] == "customer.subscription.paused":
        subscription: stripe.Subscription = event["data"]["object"]

        if user := getUser(subscription.customer):
            user.subscription_on = False
            user.save()

    elif event["type"] == "customer.subscription.resumed":
        subscription: stripe.Subscription = event["data"]["object"]

        if user := getUser(subscription.customer):
            user.subscription_on = True
            user.save()

    elif event["type"] == "customer.subscription.updated":
        subscription: stripe.Subscription = event["data"]["object"]

        if user := getUser(subscription.customer):
            product = stripe.Product.retrieve(subscription.plan.product)
            user.membership = product.name.split(" ")[0]
            user.subscription_on = subscription.status == "active"
            user.save()

    LOGGER.info(event["type"])
    return dict(success=True)
