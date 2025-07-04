from .model import *


class UserLoadTo(Model):
    def __init__(
        self,
        models: "UserLoadTos",
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


class UserLoadTos(Models):
    model_class = UserLoadTo


UserLoadTos = UserLoadTos()
