from typing import List

from pydantic import BaseModel


class PlaceCreate(BaseModel):
    pin: str
    place_name: str
    parent_place: str
    latitude: float
    longitude: float


class Place(PlaceCreate):
    accuracy: int

    class Config:
        orm_mode = True
