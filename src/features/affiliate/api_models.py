from typing import Optional
from datetime import datetime
from ...shared.services.routers.api_models import *


class Campaign(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str


class Link(BaseModel):
    id: str
    url: str
    token: str
    visitors: int
    leads: int
    conversions: int


class Coupon(BaseModel):
    id: str
    external_id: str
    token: str
    leads: int
    conversions: int
    affiliate_id: str


class CurrencyValue(BaseModel):
    cents: int
    currency_iso: str


class Currency(BaseModel):
    unpaid: CurrencyValue
    due: CurrencyValue
    paid: CurrencyValue
    total: CurrencyValue
    gross_revenue: CurrencyValue
    net_revenue: CurrencyValue


class CommissionStats(BaseModel):
    currencies: dict[str, Currency]


class Affiliate(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    state: str
    first_name: str
    last_name: str
    email: str
    confirmed_at: datetime
    # paypal_email: Optional[str] = None
    # paypal_email_confirmed_at: Optional[datetime] = None
    # wise_email: Optional[str] = None
    # wise_email_confirmed_at: Optional[datetime] = None
    # receive_new_commission_notifications: bool
    sign_in_count: int
    # unconfirmed_email: Optional[str] = None
    # stripe_customer_id: str
    # stripe_account_id: str
    visitors: int
    leads: int
    conversions: int
    # campaign: Campaign
    links: list[Link]
    # coupons: list[Coupon]
    # commission_stats: CommissionStats


class AffiliateResponse(Response):
    affiliate: Affiliate
