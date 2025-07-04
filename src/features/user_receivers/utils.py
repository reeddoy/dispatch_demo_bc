from ...models import *
from .api_models import *


def getUserReceiverResponse(
    user_receiver: UserReceiver, detail: str
) -> UserReceiverResponse:
    return UserReceiverResponse(
        detail=detail,
        user_receiver=UserReceiverModel(
            id=user_receiver.id,
            user_id=user_receiver.user_id,
            contact_person=user_receiver.contact_person,
            company_name=user_receiver.company_name,
            phone_number=user_receiver.phone_number,
            notes=user_receiver.notes,
        ),
    )
