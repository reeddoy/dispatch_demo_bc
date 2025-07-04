from ...shared.services.routers.api_models import *

# class

# create_customer
# create_subscription
# cancel_subscription
# update_subscription
# preview_invoice
# webhook_received


class Price(BaseModel):
    id: str
    currency: str
    product: str
    unit_amount: int


class PricesResponse(Response):
    prices: list[Price]


class Package(BaseModel):
    id: str
    name: str
    default_price: str


class PackagesResponse(Response):
    packages: list[Package]


class CheckOutSessionRequest(BaseModel):
    success_url: str
    cancel_url: str


class CheckOutSessionResponse(Response):
    session_url: str


class PortalSessionRequest(BaseModel):
    return_url: str


class PortalSessionResponse(Response):
    session_url: str
