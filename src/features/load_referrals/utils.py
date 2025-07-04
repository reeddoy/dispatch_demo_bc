from ...models import LoadReferral
from ...shared.within_proximity import *
from .api_models import SearchLoadReferralRequest, LoadReferralModel


def filter_load_referrals(
    load_referrals: list[LoadReferral],
    request: SearchLoadReferralRequest,
) -> bool:
    searched_load_referrals: list[LoadReferral] = []
    non_matched: list[LoadReferral] = []

    for load_referral in load_referrals:
        if (
            (request.pickup and str(request.pickup) == str(load_referral.pickup))
            or (request.length and str(request.length) == str(load_referral.length))
            or (
                request.equipment_type
                and str(request.equipment_type) == str(load_referral.equipment_type)
            )
            or (
                request.delivery
                and str(request.delivery) == str(load_referral.delivery)
            )
            or (request.weight and str(request.weight) == str(load_referral.weight))
            or (
                request.full_or_partial
                and str(request.full_or_partial) == str(load_referral.full_or_partial)
            )
            or (
                request.trip_miles
                and str(request.trip_miles) == str(load_referral.trip_miles)
            )
            or (
                request.origin
                and (
                    compareExact(request.origin, load_referral.origin)
                    or compareFirst(request.origin, load_referral.origin)
                )
            )
            or (
                request.destination
                and (
                    compareExact(request.destination, load_referral.destination)
                    or compareFirst(request.destination, load_referral.destination)
                )
            )
            or (request.origin and compareFirst(request.origin, load_referral.origin))
            or (
                request.destination
                and compareFirst(request.destination, load_referral.destination)
            )
        ):
            searched_load_referrals.append(load_referral)
        else:
            non_matched.append(load_referral)

    close_matched: list[LoadReferral] = []
    for load_referral in non_matched:
        if (
            bool(
                request.origin_latitude
                and request.origin_longitude
                and load_referral.origin_latitude
                and load_referral.origin_longitude
            )
            and within_proximity(
                request.origin_latitude,
                request.origin_longitude,
                load_referral.origin_latitude,
                load_referral.origin_longitude,
            )
        ) or (
            bool(
                request.destination_latitude
                and request.destination_longitude
                and load_referral.destination_latitude
                and load_referral.destination_longitude
            )
            and within_proximity(
                request.destination_latitude,
                request.destination_longitude,
                load_referral.destination_latitude,
                load_referral.destination_longitude,
            )
        ):
            close_matched.append(load_referral)

    close_matched.sort(key=lambda obj: sort_proximity_key(request, obj))

    def sorting_key(load_referral):
        a = (
            (
                compareExact(request.origin, load_referral.origin)
                and compareExact(request.destination, load_referral.destination)
            ),
            (
                compareExact(request.origin, load_referral.origin)
                and compareFirst(request.destination, load_referral.destination)
            ),
            (
                compareFirst(request.origin, load_referral.origin)
                and compareExact(request.destination, load_referral.destination)
            ),
            (
                compareFirst(request.origin, load_referral.origin)
                and compareFirst(request.destination, load_referral.destination)
            ),
            compareExact(request.origin, load_referral.origin),
            compareExact(request.destination, load_referral.destination),
            compareFirst(request.origin, load_referral.origin),
            compareFirst(request.destination, load_referral.destination),
            bool(
                (request.pickup and (str(request.pickup) == str(load_referral.pickup)))
                or (
                    request.length
                    and (str(request.length) == str(load_referral.length))
                )
                or (
                    request.equipment_type
                    and (
                        str(request.equipment_type) == str(load_referral.equipment_type)
                    )
                )
                or (
                    request.delivery
                    and (str(request.delivery) == str(load_referral.delivery))
                )
                or (
                    request.weight
                    and (str(request.weight) == str(load_referral.weight))
                )
                or (
                    request.full_or_partial
                    and (
                        str(request.full_or_partial)
                        == str(load_referral.full_or_partial)
                    )
                )
                or (
                    request.trip_miles
                    and (str(request.trip_miles) == str(load_referral.trip_miles))
                )
            ),
        )
        return a

    searched_load_referrals.sort(key=sorting_key, reverse=True)

    return searched_load_referrals + close_matched


def get_load_referral(load_referral: LoadReferral) -> LoadReferralModel:
    return LoadReferralModel(
        id=load_referral.id,
        user_id=load_referral.user_id,
        pickup=load_referral.pickup,
        delivery=load_referral.delivery,
        length=load_referral.length,
        equipment_type=load_referral.equipment_type,
        weight=load_referral.weight,
        full_or_partial=load_referral.full_or_partial,
        origin=load_referral.origin,
        destination=load_referral.destination,
        number_of_stops=load_referral.number_of_stops,
        phone_number=load_referral.phone_number,
        comments=load_referral.comments,
        rate_estimate=load_referral.rate_estimate,
        points=load_referral.points,
        xchange_rate=load_referral.xchange_rate,
        trip_miles=load_referral.trip_miles,
        origin_latitude=load_referral.origin_latitude,
        origin_longitude=load_referral.origin_longitude,
        destination_latitude=load_referral.destination_latitude,
        destination_longitude=load_referral.destination_longitude,
    )


def get_load_referrals(load_referrals: list[LoadReferral]) -> list[LoadReferralModel]:
    return [get_load_referral(load_referral) for load_referral in load_referrals]
