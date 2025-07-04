from enum import Enum


class UserType(Enum):
    dispatcher = "dispatcher"
    carrier = "carrier"
    owner = "owner"
    admin = "admin"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, Enum):
            return self.value == other.value
        return False


class ChatType(Enum):
    private = "private"
    lounge = "lounge"


# class ServiceArea(Enum):
#     north = "north"
#     east = "east"
#     south = "south"
#     west = "west"
#     north_east = "north_east"
#     north_west = "north_west"
#     south_east = "south_east"
#     south_west = "south_west"
