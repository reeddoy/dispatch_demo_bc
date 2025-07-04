from .model import *


class Load(Model):
    def __init__(
        self,
        models: "Loads",
        *,
        user_id: str,
        user_type: str,
        load_type: str,
        equipment_type: str,
        load_id: int,
        status: str,
        truck: str,
        bill_to: str,
        rate: float,
        trailer: str,
        load_manager: str,
        name: str,
        shippers: list[dict] = [],
        receivers: list[dict] = [],
        other_charges: list[dict] = [],
        note: str = "",
        origin: str = "",
        destination: str = "",
        files: list[str] = [],
        origin_latitude: float = None,
        origin_longitude: float = None,
        destination_latitude: float = None,
        destination_longitude: float = None,
        hours: float = None,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.user_type = user_type
        self.load_type = load_type
        self.equipment_type = equipment_type
        self.load_id = load_id
        self.status = status
        self.truck = truck
        self.bill_to = bill_to
        self.rate = rate
        self.trailer = trailer
        self.load_manager = load_manager
        self.name = name
        self.shippers = shippers
        self.receivers = receivers
        self.other_charges = other_charges
        self.note = note
        self.origin = origin
        self.destination = destination
        self.files = files
        self.origin_latitude = origin_latitude
        self.origin_longitude = origin_longitude
        self.destination_latitude = destination_latitude
        self.destination_longitude = destination_longitude
        self.hours = hours


class Loads(Models):
    model_class = Load


Loads = Loads()
