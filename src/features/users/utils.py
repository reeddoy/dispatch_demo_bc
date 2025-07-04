from ...constants.enums import UserType
from ...models.user import User


def filter_dispatchers(user: User) -> bool:
    return user and user.user_type == UserType.dispatcher


def filter_carriers(user: User) -> bool:
    return user and user.user_type == UserType.carrier


def filter_owners(user: User) -> bool:
    return user and user.user_type == UserType.owner


def filter_not_owners(user: User) -> bool:
    return user and user.user_type != UserType.owner
