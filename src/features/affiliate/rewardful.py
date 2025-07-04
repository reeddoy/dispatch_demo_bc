import requests
from requests.auth import HTTPBasicAuth

from ...constants.config import *
from .api_models import *


class AffiliateData(BaseModel):
    data: Affiliate


class Rewardful:
    root = "https://api.getrewardful.com/v1"

    api_key = "a0b2f4"

    def request(
        self,
        path: str,
        json: dict = {},
        data: dict = {},
        params: dict = {},
        method: str = "GET",
    ) -> dict:
        url = f"{self.root}/{path}"
        response = requests.request(
            method,
            url,
            auth=HTTPBasicAuth(REWARDFUL, ""),
            json=json,
            params=params,
            data=data,
        )

        return response.json()

    def campaigns(self) -> dict:
        return self.request("campaigns")

    def campaign(self, id: str) -> dict:
        return self.request(f"campaigns/{id}")

    def affiliates(self) -> dict:
        return self.request("affiliates")

    def affiliate(self, id: str) -> dict:
        return self.request(f"affiliates/{id}")

    def create_affiliate(
        self,
        first_name: str,
        last_name: str,
        email: str,
        stripe_customer_id: str,
    ) -> AffiliateData:
        return self.request(
            "affiliates",
            data=dict(
                first_name=first_name,
                last_name=last_name,
                email=email,
                stripe_customer_id=stripe_customer_id,
            ),
            method="POST",
        )

    def create_affiliate_link(self, affiliate_id: str) -> dict:
        return self.request(
            "affiliate_links",
            data=dict(affiliate_id=affiliate_id),
            method="POST",
        )

    def affiliate_link(self, id: str) -> dict:
        return self.request(f"affiliate_links/{id}")
