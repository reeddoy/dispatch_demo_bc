from ...models import UserBillTo
from .api_models import *


def getUserBillToResponse(user_bill_to: UserBillTo, detail: str) -> UserBillToResponse:
    return UserBillToResponse(
        detail=detail,
        user_bill_to=UserBillToModel(
            id=user_bill_to.id,
            user_id=user_bill_to.user_id,
            company_name=user_bill_to.company_name,
            address=user_bill_to.address,
            phone_number=user_bill_to.phone_number,
            email=user_bill_to.email,
            notes=user_bill_to.notes,
        ),
    )
