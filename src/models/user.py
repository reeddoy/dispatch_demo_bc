from .model import *


class User(Model):
    def __init__(
        self,
        models: "Users",
        *,
        user_type: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        company_name: str = "",
        image: str = "",
        address: str = "",
        referral: str = "",
        affiliate_id: str = "",
        phone_number: str = "",
        user_name: str = "",
        website: str = "",
        service_areas: list[str] = [],
        dispatche_fees: list[str] = [],
        accept_new_authorities: bool = False,
        ein: str = "",
        mc: str = "",
        dot: str = "",
        offered_services: list[str] = [],
        equipment_types: list[str] = [],
        description: str = "",
        verified: bool = False,
        saved_loads: list[str] = [],
        saved_trucks: list[str] = [],
        favourites: list[str] = [],
        membership: str = "",
        on_trial: bool = False,
        trial_complete: bool = False,
        active: bool = False,
        customer_id: str = "",
        account_id: str = "",
        contacts: list = [],
        otp: int = 0,
        subscription_on: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_type = user_type
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.image = image
        self.address = address
        self.referral = referral
        self.affiliate_id = affiliate_id
        self.phone_number = phone_number
        self.user_name = user_name
        self.website = website
        self.service_areas = service_areas
        self.dispatche_fees = dispatche_fees
        self.accept_new_authorities = accept_new_authorities
        self.ein = ein
        self.mc = mc
        self.dot = dot
        self.offered_services = offered_services
        self.equipment_types = equipment_types
        self.description = description
        self.verified = verified
        self.saved_loads = saved_loads
        self.saved_trucks = saved_trucks
        self.favourites = favourites
        self.membership = membership
        self.on_trial = on_trial
        self.trial_complete = trial_complete
        self.active = active
        self.customer_id = customer_id
        self.account_id = account_id
        self.contacts = contacts
        self.otp = otp
        self.subscription_on = subscription_on


class Users(Models):
    model_class = User


Users = Users()
