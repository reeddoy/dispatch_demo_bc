from datetime import datetime
import geopy.distance


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

    def calculate_proximity_score(self, search_origin, search_destination):
        """
        Calculates a proximity score based on the distance from the search origin and destination.
        Lower scores are better, with exact matches having the highest priority.
        """
        # Dummy implementation for coordinates; replace with real geocoding
        origin_coords = (0, 0)  # Replace with real coordinates
        destination_coords = (0, 0)  # Replace with real coordinates
        search_origin_coords = (0, 0)  # Replace with real coordinates
        search_destination_coords = (0, 0)  # Replace with real coordinates

        # Calculate distances
        distance_to_origin = geopy.distance.distance(
            origin_coords, search_origin_coords
        ).miles
        distance_to_destination = geopy.distance.distance(
            destination_coords, search_destination_coords
        ).miles

        # Combine distances into a single score
        return distance_to_origin + distance_to_destination


def search_loads(search_date, search_origin, search_destination, load_list):
    # Parse search_date to datetime
    search_date = datetime.strptime(search_date, "%m/%d/%Y")

    exact_matches = []
    non_exact_matches = []

    for load in load_list:
        load_pickup_date = datetime.strptime(load.pickup, "%m/%d/%Y")
        load_delivery_date = datetime.strptime(load.delivery, "%m/%d/%Y")

        if (
            load_pickup_date == search_date
            and load.delivery == search_date.strftime("%m/%d/%Y")
            and load.origin == search_origin
            and load.destination == search_destination
        ):
            exact_matches.append(load)
        else:
            non_exact_matches.append(load)

    # Sort exact matches by date
    exact_matches.sort(key=lambda l: datetime.strptime(l.pickup, "%m/%d/%Y"))

    # Sort non-exact matches by proximity score
    non_exact_matches.sort(
        key=lambda l: l.calculate_proximity_score(search_origin, search_destination)
    )

    return exact_matches + non_exact_matches


def geocode(address):
    """
    Dummy geocode function. Replace with actual geocoding logic.
    """
    return (0, 0)  # Replace with actual coordinates from a geocoding service
