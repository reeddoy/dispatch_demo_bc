from ...models import Truck
from ...shared.within_proximity import *
from .api_models import SearchTruckRequest


def filter_trucks(
    trucks: list[Truck],
    request: SearchTruckRequest,
) -> bool:
    searched_trucks: list[Truck] = []
    non_matched: list[Truck] = []

    for truck in trucks:
        if (
            (request.pickup and str(request.pickup) == str(truck.pickup))
            or (request.length and str(request.length) == str(truck.length))
            or (
                request.equipment_type
                and str(request.equipment_type) == str(truck.equipment_type)
            )
            or (request.delivery and str(request.delivery) == str(truck.delivery))
            or (
                request.available_point
                and str(request.available_point) == str(truck.available_point)
            )
            or (request.weight and str(request.weight) == str(truck.weight))
            or (
                request.full_or_partial
                and str(request.full_or_partial) == str(truck.full_or_partial)
            )
            or (request.trip_miles and str(request.trip_miles) == str(truck.trip_miles))
            or (
                request.origin
                and (
                    compareExact(request.origin, truck.origin)
                    or compareFirst(request.origin, truck.origin)
                )
            )
            or (
                request.destination
                and (
                    compareExact(request.destination, truck.destination)
                    or compareFirst(request.destination, truck.destination)
                )
            )
            or (request.origin and compareFirst(request.origin, truck.origin))
            or (
                request.destination
                and compareFirst(request.destination, truck.destination)
            )
        ):
            searched_trucks.append(truck)
        else:
            non_matched.append(truck)

    close_matched: list[Truck] = []
    for truck in non_matched:
        if (
            bool(
                request.origin_latitude
                and request.origin_longitude
                and truck.origin_latitude
                and truck.origin_longitude
            )
            and within_proximity(
                request.origin_latitude,
                request.origin_longitude,
                truck.origin_latitude,
                truck.origin_longitude,
            )
        ) or (
            bool(
                request.destination_latitude
                and request.destination_longitude
                and truck.destination_latitude
                and truck.destination_longitude
            )
            and within_proximity(
                request.destination_latitude,
                request.destination_longitude,
                truck.destination_latitude,
                truck.destination_longitude,
            )
        ):
            close_matched.append(truck)

    close_matched.sort(key=lambda obj: sort_proximity_key(request, obj))

    def sorting_key(truck):
        a = (
            (
                compareExact(request.origin, truck.origin)
                and compareExact(request.destination, truck.destination)
            ),
            (
                compareExact(request.origin, truck.origin)
                and compareFirst(request.destination, truck.destination)
            ),
            (
                compareFirst(request.origin, truck.origin)
                and compareExact(request.destination, truck.destination)
            ),
            (
                compareFirst(request.origin, truck.origin)
                and compareFirst(request.destination, truck.destination)
            ),
            compareExact(request.origin, truck.origin),
            compareExact(request.destination, truck.destination),
            compareFirst(request.origin, truck.origin),
            compareFirst(request.destination, truck.destination),
            bool(
                (request.pickup and (str(request.pickup) == str(truck.pickup)))
                or (request.length and (str(request.length) == str(truck.length)))
                or (
                    request.equipment_type
                    and (str(request.equipment_type) == str(truck.equipment_type))
                )
                or (request.delivery and (str(request.delivery) == str(truck.delivery)))
                or (
                    request.available_point
                    and (str(request.available_point) == str(truck.available_point))
                )
                or (request.weight and (str(request.weight) == str(truck.weight)))
                or (
                    request.full_or_partial
                    and (str(request.full_or_partial) == str(truck.full_or_partial))
                )
                or (
                    request.trip_miles
                    and (str(request.trip_miles) == str(truck.trip_miles))
                )
            ),
        )
        return a

    searched_trucks.sort(key=sorting_key, reverse=True)

    return searched_trucks + close_matched
