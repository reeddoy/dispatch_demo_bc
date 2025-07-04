from datetime import datetime
from urllib.parse import urlparse
from ...models import Load
from ...shared.services.storage import *
from ...shared.within_proximity import *
from .api_models import *


def get_date_tuple(d: int) -> tuple[int, int, int]:
    date = datetime.fromtimestamp(d / 1000)
    return (date.year, date.month, date.day)


def compare_dates(a: int, b: int) -> bool:
    a = get_date_tuple(a)
    b = get_date_tuple(b)
    return a == b


def compare_load_attributes(load: Load, request: SearchLoadRequest) -> bool:
    return bool(
        (request.user_type and str(request.user_type) == str(load.user_type))
        or (request.load_type and str(request.load_type) == str(load.load_type))
        or (
            request.equipment_type
            and str(request.equipment_type) == str(load.equipment_type)
        )
        or (request.status and str(request.status) == str(load.status))
        or (request.truck and str(request.truck) == str(load.truck))
        or (request.bill_to and str(request.bill_to) == str(load.bill_to))
        or (request.trailer and str(request.trailer) == str(load.trailer))
        or (
            request.load_manager and str(request.load_manager) == str(load.load_manager)
        )
        or (request.name and str(request.name) == str(load.name))
        or (request.note and str(request.note) == str(load.note))
        or (request.rate and str(request.rate) == str(load.rate))
        or (request.hours and str(request.hours) == str(load.hours))
        or (request.load_id and str(request.load_id) == str(load.load_id))
        or (
            request.shipper
            and (
                True
                in [
                    str(request.shipper) == str(shipper.get("name"))
                    for shipper in load.shippers
                ]
            )
        )
        or (
            request.receiver
            and (
                True
                in [
                    str(request.receiver) == str(receiver.get("name"))
                    for receiver in load.receivers
                ]
            )
        )
        or (
            request.ship_date
            and (
                True
                in [
                    compare_dates(
                        request.ship_date,
                        shipper.get("date", 0),
                    )
                    for shipper in load.shippers
                ]
            )
        )
        or (
            request.delivery_date
            and (
                True
                in [
                    compare_dates(
                        request.delivery_date,
                        receiver.get("date", 0),
                    )
                    for receiver in load.receivers
                ]
            )
        )
    )


def filter_loads(
    loads: list[Load],
    request: SearchLoadRequest,
) -> bool:
    searched_loads: list[Load] = []
    non_matched: list[Load] = []

    for load in loads:
        if (
            compare_load_attributes(load, request)
            or (
                request.origin
                and (
                    compareExact(request.origin, load.origin)
                    or compareFirst(request.origin, load.origin)
                )
            )
            or (
                request.destination
                and (
                    compareExact(request.destination, load.destination)
                    or compareFirst(request.destination, load.destination)
                )
            )
            or (request.origin and compareFirst(request.origin, load.origin))
            or (
                request.destination
                and compareFirst(request.destination, load.destination)
            )
        ):
            searched_loads.append(load)
        else:
            non_matched.append(load)

    close_matched: list[Load] = []
    for load in non_matched:
        if (
            bool(
                request.origin_latitude
                and request.origin_longitude
                and load.origin_latitude
                and load.origin_longitude
            )
            and within_proximity(
                request.origin_latitude,
                request.origin_longitude,
                load.origin_latitude,
                load.origin_longitude,
            )
        ) or (
            bool(
                request.destination_latitude
                and request.destination_longitude
                and load.destination_latitude
                and load.destination_longitude
            )
            and within_proximity(
                request.destination_latitude,
                request.destination_longitude,
                load.destination_latitude,
                load.destination_longitude,
            )
        ):
            close_matched.append(load)

    close_matched.sort(key=lambda obj: sort_proximity_key(request, obj))

    def sorting_key(load):
        a = (
            (
                compareExact(request.origin, load.origin)
                and compareExact(request.destination, load.destination)
            ),
            (
                compareExact(request.origin, load.origin)
                and compareFirst(request.destination, load.destination)
            ),
            (
                compareFirst(request.origin, load.origin)
                and compareExact(request.destination, load.destination)
            ),
            (
                compareFirst(request.origin, load.origin)
                and compareFirst(request.destination, load.destination)
            ),
            compareExact(request.origin, load.origin),
            compareExact(request.destination, load.destination),
            compareFirst(request.origin, load.origin),
            compareFirst(request.destination, load.destination),
            compare_load_attributes(load, request),
        )
        return a

    searched_loads.sort(key=sorting_key, reverse=True)

    return searched_loads + close_matched


def get_files(files: list[str]) -> list[Url]:
    file_urls = []

    for file in files:
        url = get_signed_url(file)
        path = urlparse(file).path
        _, *names = path.split("-")
        name = "".join(names)
        file_urls.append(Url(name=name, url=url))

    return file_urls


def get_load(load: Load) -> LoadModel:
    return LoadModel(
        user_type=load.user_type,
        load_type=load.load_type,
        equipment_type=load.equipment_type,
        status=load.status,
        truck=load.truck,
        bill_to=load.bill_to,
        rate=load.rate,
        hours=load.hours,
        trailer=load.trailer,
        load_manager=load.load_manager,
        name=load.name,
        note=load.note,
        shippers=load.shippers,
        receivers=load.receivers,
        other_charges=load.other_charges,
        files=get_files(load.files),
        id=load.id,
        user_id=load.user_id,
        load_id=load.load_id,
        origin=load.origin,
        destination=load.destination,
    )


def get_loads(loads: list[Load]) -> list[LoadModel]:
    return [get_load(load) for load in loads]
