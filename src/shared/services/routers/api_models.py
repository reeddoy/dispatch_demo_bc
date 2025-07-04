from pydantic import BaseModel as _BaseModel
from enum import Enum


class BaseModel(_BaseModel):
    def model_dump(self):
        clean_dump = {}

        for k, v in super().model_dump().items():
            if isinstance(v, Enum):
                v: Enum
                v = v.value

            clean_dump[k] = v

        return clean_dump


class Response(BaseModel):
    detail: str


class Media(BaseModel):
    filename: str
    data: str
