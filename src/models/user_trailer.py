from .model import *


class UserTrailer(Model):
    def __init__(
        self,
        models: "UserTrailers",
        *,
        user_id: str,
        trailer_number: str,
        year: str,
        make: str,
        model: str,
        tag_number: str,
        notes: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.user_id = user_id
        self.trailer_number = trailer_number
        self.year = year
        self.make = make
        self.model = model
        self.tag_number = tag_number
        self.notes = notes


class UserTrailers(Models):
    model_class = UserTrailer


UserTrailers = UserTrailers()
