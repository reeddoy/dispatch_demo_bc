import stripe
from ...shared.services.routers.utils import *
from .api_models import *


def create_checkout_session(
    package: str,
    request: CheckOutSessionRequest,
    session: Session = get_session,
) -> CheckOutSessionResponse:
    products = stripe.Product.search(query=f"name:'{package}'").data

    if not products:
        raise HTTPException(HTTP_400_BAD_REQUEST)

    product = products[0]

    user = session.user

    subscription_data = dict()
    if user.membership or user.trial_complete:
        ...

    else:
        subscription_data.update(trial_period_days=30 if package == "Premium" else 7),

    checkStripeCustomer(user)

    kwargs = dict()

    if user.referral:
        kwargs.update(client_reference_id=user.referral)

    checkout_session = stripe.checkout.Session.create(
        customer=user.customer_id,
        success_url=request.success_url,
        cancel_url=request.cancel_url,
        payment_method_types=["card"],
        allow_promotion_codes=True,
        mode="subscription",
        line_items=[dict(price=product.default_price, quantity=1)],
        metadata=dict(user_id=user.id, package=package),
        subscription_data=subscription_data,
        **kwargs,
    )

    return CheckOutSessionResponse(
        detail=f"Checked out for {package} successfully.",
        session_url=checkout_session.url,
    )


def checkStripeCustomer(user: User):
    if user.customer_id:
        try:
            stripe.Customer.retrieve(user.customer_id)
        except:
            user.customer_id = ""

    if not user.customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            name=f"{user.first_name} {user.last_name}",
            phone=user.phone_number,
            metadata=dict(user_id=user.id),
        )
        user.customer_id = customer.id
        user.save()


def getUser(customer_id: str) -> None | User:
    session = Sessions.get_by_customer_id(customer_id)
    return session.user if session else Users.get_one("customer_id", customer_id)
