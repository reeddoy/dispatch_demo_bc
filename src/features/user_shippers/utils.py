from ...models import *
from .api_models import *


def getUserShipperResponse(
    user_shipper: UserShipper, detail: str
) -> UserShipperResponse:
    return UserShipperResponse(
        detail=detail,
        user_shipper=UserShipperModel(
            id=user_shipper.id,
            user_id=user_shipper.user_id,
            contact_person=user_shipper.contact_person,
            company_name=user_shipper.company_name,
            phone_number=user_shipper.phone_number,
            notes=user_shipper.notes,
        ),
    )
