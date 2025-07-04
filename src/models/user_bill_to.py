from .model import *


class UserBillTo(Model):
    def __init__(
        self,
        models: "UserBillTos",
        *,
        user_id: str,
        company_name: str,
        address: str,
        phone_number: str,
        email: str,
        notes: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.company_name = company_name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.notes = notes


class UserBillTos(Models):
    model_class = UserBillTo


UserBillTos = UserBillTos()
