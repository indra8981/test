from typing import Tuple

from simplejson.tests.test_namedtuple import Point
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Place(Base):
    __tablename__ = "Geog"
    pin = Column(String, unique=True, primary_key=True, index=True)
    place_name = Column(String, index=True)
    parent_place = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    accuracy = Column(Integer, default=6)
