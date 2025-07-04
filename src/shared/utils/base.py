from typing import Any, Callable
from .commons import get_id, get_timestamp


def modifier(method: Callable):
    def wrapper(self: Base, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.modified()
        return result

    return wrapper


class Base:
    keys_to_remove_on_dict: list[str] = []

    def __bool__(self):
        return True

    def __init__(self):
        self.alive = True
        self.modified_timestamp: int = get_timestamp()

    def kill(self):
        self.alive = False

    def modified(self):
        self.modified_timestamp = get_timestamp()


class Child(Base):
    def __init__(self, id: str = None):
        Base.__init__(self)

        self.id = id or get_id()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id=`{self.id}`)"

    def __repr__(self) -> str:
        return f"<{self}>"


class Manager(Base):
    property_key = "id"

    def __init__(self):
        Base.__init__(self)

        self.children: dict[str, Child] = {}

    def values(self) -> list[Child]:
        return list(self.children.values())

    def get(self, property_key: str) -> Child:
        return self.children.get(property_key)

    def get_by(self, property: str, value: str):
        return list(
            filter(
                lambda user: getattr(user, property, None) == value,
                self.children.values(),
            )
        )

    def get_one_by(self, property: str, value: str):
        filtered_children = self.get_by(property, value)
        if filtered_children:
            return filtered_children[0]

    def get_one_by_email(self, email: str):
        return self.get_one_by("email", email)

    def is_child(self, key: str) -> bool:
        return key in self.children

    @modifier
    def add_child(self, child: Child) -> bool:
        property = getattr(child, self.property_key, None)
        if (property != None) and not self.is_child(property):
            self.children[property] = child
            return True
        return False

    def remove_child(self, child: Child) -> bool:
        property = getattr(child, self.property_key, None)

        if (property != None) and (property in self.children):
            del self.children[property]
            return True
        return False


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        instance = cls._instances[cls]
        return instance


class Singleton(metaclass=_Singleton):
    ...


class SingletonChild(Child, metaclass=_Singleton):
    ...


class SingletonManager(Manager, metaclass=_Singleton):
    ...
