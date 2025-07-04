import math
import os, enum, string
from bson import ObjectId
from pymongo import *
import pymongo
from pymongo.database import Database, Collection

from ..constants.config import *
from ..shared.utils.base import Singleton
from ..shared.utils.commons import get_id, get_timestamp, hash_bcrypt


class Model:
    property_to_remove_on_db_dump = ["models"]

    def __init__(
        self,
        models: "Models",
        _id: str = "",
        id: str = "",
        created_timestamp: int = 0,
        **kwargs,
    ) -> None:
        self.models = models

        self._id = _id
        self.id = id
        self.created_timestamp = created_timestamp

    @property
    def dict(self) -> dict:
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, enum.Enum):
                v = v.value
            if k not in self.property_to_remove_on_db_dump:
                d[k] = v
        return d

    @property
    def db_dump(self) -> dict:
        _dict = self.dict
        del _dict["_id"]
        return _dict

    def save(self):
        self.models.update_child(self)

    def delete(self):
        self.models.delete_child(self._id)

    def update(self, **kwargs):
        if password := kwargs.get("password"):
            kwargs.update(password=hash_bcrypt(password))

        for key, value in kwargs.items():
            if hasattr(self, key) and value:
                setattr(self, key, value)
        self.save()


class Models(Singleton):
    model_class = Model
    MONGO: MongoClient = None
    DATABASE: Database = None

    def __init__(self):
        Singleton.__init__(self)

        if not Models.MONGO:
            LOGGER.info(f"Connecting to MongoDB on {MONGODB}.")
            Models.MONGO = MongoClient(MONGODB)
            Models.MONGO.admin.command("ping")
            Models.DATABASE = Models.MONGO["dispatchXchanger"]

            LOGGER.info(
                "Pinged your deployment. You successfully connected to MongoDB!"
            )
        else:
            collections = Models.DATABASE.list_collection_names()
            if self.name not in collections:
                Models.DATABASE.create_collection(self.name)

        # self.collection.create_index("id", unique=True)

    @property
    def name(self) -> str:
        underscore = "_"
        ns = ""
        for n in self.__class__.__name__:
            if n in string.ascii_uppercase:
                n = f"{underscore}{n.lower()}"
            ns += n
        ns = ns.strip(underscore)
        return ns

    @property
    def collection(self) -> Collection:
        return Models.DATABASE[self.name]

    def child_exists(self, key: str, value: str) -> bool:
        return bool(self.find_one({key: value}))

    def exists(self, id: str) -> bool:
        c = self.count_documents({"id": id})
        k = bool(c)
        return k

    def get_child(self, id: str) -> Model | None:
        # return self.find_one({"_id": ObjectId(id)})
        return self.find_one({"id": id})

    def delete_children(self, filters: dict = {}):
        self.collection.delete_many(filters)

    def delete_child(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})
        return True

    def count_documents(self, filters: dict = {}) -> int:
        return self.collection.count_documents(filters)

    def count_pages(self, limit: int, filters: dict = {}) -> int:
        if not limit:
            return 0
        count = self.collection.count_documents(filters)
        return math.ceil(count / limit)

    @property
    def count(self) -> int:
        return self.count_documents()

    def create(
        self,
        id: str = "",
        created_timestamp: int = 0,
        **kwargs,
    ) -> Model:
        if password := kwargs.get("password"):
            kwargs.update(password=hash_bcrypt(password))

        if pin := kwargs.get("pin"):
            kwargs.update(pin=hash_bcrypt(pin))

        kwargs.update(
            id=id or get_id(),
            created_timestamp=created_timestamp or get_timestamp(),
        )

        model = self.model_class(self, **kwargs)
        p = self.collection.insert_one(model.db_dump)
        model._id = str(p.inserted_id)

        return model

    def update_many(self, filter: dict, update: dict):
        self.collection.update_many(filter, update)

    def get(self, child_key: str = "", equal_to=None):
        fil = {}
        if child_key and equal_to:
            fil = {child_key: equal_to}
        return self.find(fil)

    def get_one(self, child_key: str = "", equal_to=None):
        fil = {}
        if child_key and equal_to:
            fil = {child_key: equal_to}
        return self.find_one(fil)

    def find(
        self,
        filters: dict = {},
        limit: int = 0,
        skip: int = 0,
        sort: list[str] | str = None,
        descending: bool = False,
        search_or: list | dict = [],
        search_and: list | dict = [],
    ):
        filters = filters.copy()
        if search_or:
            so = search_or.copy()
            if isinstance(so, dict):
                _or = []
                for k, v in so.items():
                    if v:
                        if isinstance(v, str):
                            v = {"$regex": v, "$options": "i"}
                        _or.append({k: v})

                so = _or
            filters["$or"] = so

        if search_and:
            sa = search_and.copy()
            if isinstance(sa, dict):
                _and = []
                for k, v in search_and.items():
                    if v:
                        if isinstance(v, str):
                            v = {"$regex": v, "$options": "i"}
                        _and.append({k: v})
                sa = _and
            filters["$and"] = sa

        items = self.collection.find(filters)
        if skip > 0:
            items = items.skip(skip)
        if limit:
            items = items.limit(limit)
        if sort:
            items = items.sort(
                sort,
                direction=pymongo.DESCENDING if descending else pymongo.ASCENDING,
            )
        # items = list(items)
        items_ = []
        for item in items:
            try:
                items_.append(self.model_class(self, **item))
            except Exception as e:
                print(e, item)
                ...
        return items_

    def find_one(self, filters: dict = {}):
        one = self.collection.find_one(filters)
        if one:
            return self.model_class(self, **one)

    def update_child(self, child: Model):
        self.collection.update_one(
            {"_id": ObjectId(child._id)}, {"$set": child.db_dump}
        )

    def drop(self):
        self.collection.drop()
