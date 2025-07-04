import math


def compareExact(a: str, b: str) -> bool:
    return bool(a and (a.lower().strip().replace(" ", "") in b.lower()))


def compareFirst(a: str, b: str) -> bool:
    alist = a.split(",")
    alist = [a.strip(" ").strip(",") for a in alist if a]
    return bool(alist and (alist[0].lower() in b.lower()))


def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in miles
    R = 3958.8

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in miles
    distance = R * c

    return abs(distance)


def within_proximity(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
):
    distance = haversine_distance(
        lat1,
        lon1,
        lat2,
        lon2,
    )
    return distance <= 150


def sort_proximity_key(request, obj):
    a = (
        haversine_distance(
            request.origin_latitude,
            request.origin_longitude,
            obj.origin_latitude,
            obj.origin_longitude,
        )
        if bool(
            request.origin_latitude
            and request.origin_longitude
            and obj.origin_latitude
            and obj.origin_longitude
        )
        else 200
    )
    b = (
        haversine_distance(
            request.destination_latitude,
            request.destination_longitude,
            obj.destination_latitude,
            obj.destination_longitude,
        )
        if bool(
            request.destination_latitude
            and request.destination_longitude
            and obj.destination_latitude
            and obj.destination_longitude
        )
        else 200
    )
    return a, b
