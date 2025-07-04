from .model import *


class UserTruck(Model):
    def __init__(
        self,
        models: "UserTrucks",
        *,
        user_id: str,
        truck_number: str,
        year: str,
        make: str,
        model: str,
        tag_number: str,
        notes: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.truck_number = truck_number
        self.year = year
        self.make = make
        self.model = model
        self.tag_number = tag_number
        self.notes = notes


class UserTrucks(Models):
    model_class = UserTruck


UserTrucks = UserTrucks()
