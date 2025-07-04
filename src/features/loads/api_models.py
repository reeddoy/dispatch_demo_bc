from typing import Optional
from ...shared.services.routers.api_models import *


class Charge(BaseModel):
    amount: float
    charge: str


class Shipper(BaseModel):
    name: str
    notes: str
    location: str
    date: int
    weight: float
    p_o_numbers: str
    # description: str
    # type: str
    # quantity: float


class Url(BaseModel):
    name: str
    url: str


class NewLoadRequest(BaseModel):
    user_type: str
    load_type: str
    equipment_type: str
    status: str
    truck: str
    bill_to: str
    rate: float
    trailer: str
    load_manager: str
    name: str
    note: str

    hours: float

    origin: Optional[str] = ""
    destination: Optional[str] = ""

    shippers: Optional[list[Shipper]] = []
    receivers: Optional[list[Shipper]] = []
    other_charges: Optional[list[Charge]] = []

    files: Optional[list[Media]] = []

    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0


class PatchLoadRequest(BaseModel):
    user_type: Optional[str] = ""
    load_type: Optional[str] = ""
    equipment_type: Optional[str] = ""
    status: Optional[str] = ""
    truck: Optional[str] = ""
    bill_to: Optional[str] = ""
    rate: Optional[float] = 0.0
    hours: Optional[float] = 0.0
    trailer: Optional[str] = ""
    load_manager: Optional[str] = ""
    name: Optional[str] = ""

    shippers: Optional[list[Shipper]] = []
    receivers: Optional[list[Shipper]] = []
    other_charges: Optional[list[Charge]] = []


class LoadModel(BaseModel):
    user_type: str
    load_type: str
    equipment_type: str
    status: str
    truck: str
    bill_to: str
    rate: float
    trailer: str
    load_manager: str
    name: str
    note: str

    origin: str
    destination: str

    shippers: list[Shipper]
    receivers: list[Shipper]
    other_charges: list[Charge]

    id: str
    user_id: str
    load_id: int
    files: list[Url]

    hours: Optional[float] = 0
    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0


class LoadsResponse(Response):
    loads: list[LoadModel]
    pages: Optional[int] = 0
    page: Optional[int] = 0


class LoadResponse(Response):
    load: LoadModel


class SearchLoadRequest(BaseModel):
    user_type: Optional[str] = ""
    load_type: Optional[str] = ""
    equipment_type: Optional[str] = ""
    status: Optional[str] = ""
    truck: Optional[str] = ""

    bill_to: Optional[str] = ""
    trailer: Optional[str] = ""
    load_manager: Optional[str] = ""
    name: Optional[str] = ""
    note: Optional[str] = ""
    rate: Optional[float] = 0
    hours: Optional[float] = 0
    load_id: Optional[int] = 0
    shipper: Optional[str] = ""
    receiver: Optional[str] = ""

    ship_date: Optional[float] = 0
    delivery_date: Optional[float] = 0

    origin: Optional[str] = ""
    destination: Optional[str] = ""

    origin_latitude: Optional[float] = 0
    origin_longitude: Optional[float] = 0
    destination_latitude: Optional[float] = 0
    destination_longitude: Optional[float] = 0
