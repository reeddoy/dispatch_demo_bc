from .model import *


class LoadReferral(Model):
    def __init__(
        self,
        models: "LoadReferrals",
        *,
        user_id: str,
        pickup: str,
        delivery: str,
        full_or_partial: str,
        weight: float,
        origin: str,
        destination: str,
        number_of_stops: int,
        phone_number: str,
        equipment_type: str,
        length: float,
        comments: str,
        rate_estimate: float,
        points: int,
        xchange_rate: float,
        trip_miles: str = "",
        origin_latitude: float = None,
        origin_longitude: float = None,
        destination_latitude: float = None,
        destination_longitude: float = None,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.pickup = pickup
        self.delivery = delivery
        self.full_or_partial = full_or_partial
        self.weight = weight
        self.origin = origin
        self.destination = destination
        self.number_of_stops = number_of_stops
        self.phone_number = phone_number
        self.equipment_type = equipment_type
        self.length = length
        self.comments = comments
        self.rate_estimate = rate_estimate
        self.points = points
        self.xchange_rate = xchange_rate
        self.trip_miles = trip_miles
        self.origin_latitude = origin_latitude
        self.origin_longitude = origin_longitude
        self.destination_latitude = destination_latitude
        self.destination_longitude = destination_longitude


class LoadReferrals(Models):
    model_class = LoadReferral


LoadReferrals = LoadReferrals()
