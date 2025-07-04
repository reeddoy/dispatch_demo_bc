from ...models import *
from .api_models import *


def getUserDriverResponse(user_driver: UserDriver, detail: str) -> UserDriverResponse:
    return UserDriverResponse(
        detail=detail,
        user_driver=UserDriverModel(
            id=user_driver.id,
            user_id=user_driver.user_id,
            driver_name=user_driver.driver_name,
            address=user_driver.address,
            phone_number=user_driver.phone_number,
            email=user_driver.email,
            notes=user_driver.notes,
        ),
    )
