from .model import *


class UserDriver(Model):
    def __init__(
        self,
        models: "UserDrivers",
        *,
        user_id: str,
        driver_name: str,
        address: str,
        phone_number: str,
        email: str,
        notes: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.driver_name = driver_name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.notes = notes


class UserDrivers(Models):
    model_class = UserDriver


UserDrivers = UserDrivers()
