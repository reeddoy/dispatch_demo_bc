from .model import *


class UserReceiver(Model):
    def __init__(
        self,
        models: "UserReceivers",
        *,
        user_id: str,
        company_name: str,
        phone_number: str,
        contact_person: str,
        notes: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.company_name = company_name
        self.phone_number = phone_number
        self.contact_person = contact_person
        self.notes = notes


class UserReceivers(Models):
    model_class = UserReceiver


UserReceivers = UserReceivers()
