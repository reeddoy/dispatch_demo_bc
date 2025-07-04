from ...models import *
from .api_models import *


def getUserLoadToResponse(user_load_to: UserLoadTo, detail: str) -> UserLoadToResponse:
    return UserLoadToResponse(
        detail=detail,
        user_load_to=UserLoadToModel(
            id=user_load_to.id,
            user_id=user_load_to.user_id,
            company_name=user_load_to.company_name,
            address=user_load_to.address,
            phone_number=user_load_to.phone_number,
            email=user_load_to.email,
            notes=user_load_to.notes,
        ),
    )
