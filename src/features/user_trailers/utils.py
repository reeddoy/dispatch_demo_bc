from ...models import *
from .api_models import *


def getUserTrailerResponse(
    user_trailer: UserTrailer, detail: str
) -> UserTrailerResponse:
    return UserTrailerResponse(
        detail=detail,
        user_trailer=UserTrailerModel(
            id=user_trailer.id,
            user_id=user_trailer.user_id,
            trailer_number=user_trailer.trailer_number,
            year=user_trailer.year,
            make=user_trailer.make,
            model=user_trailer.model,
            tag_number=user_trailer.tag_number,
            notes=user_trailer.notes,
        ),
    )
