from ...models import UserTruck
from .api_models import *


def getUserTruckResponse(user_truck: UserTruck, detail: str) -> UserTruckResponse:
    return UserTruckResponse(
        detail=detail,
        user_truck=UserTruckModel(
            id=user_truck.id,
            user_id=user_truck.user_id,
            truck_number=user_truck.truck_number,
            year=user_truck.year,
            make=user_truck.make,
            model=user_truck.model,
            tag_number=user_truck.tag_number,
            notes=user_truck.notes,
        ),
    )
