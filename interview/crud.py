from sqlalchemy.orm import Session

from . import schemas, models

import math


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def check_near(db: Session, lati: float, longi: float):
    all = db.query(models.Place.latitude, models.Place.longitude).all()
    dist = distance_me(all, lati, longi, 1)
    return len(dist)


def distance_me(points, lati, longi, dist):
    all_dist = []
    for i in range(len(points)):
        two_pair_distance = distance((lati, longi), (float(points[i][0]), float(points[i][1])))
        if (two_pair_distance <= dist):
            all_dist.append(two_pair_distance)
    return all_dist


def get_place_by_longitude_latitude(db: Session, lati: float, longi: float):
    return db.query(models.Place).filter(models.Place.latitude == lati, models.Place.longitude == longi).all()


def get_place_by_pin(db: Session, pin: str, lati: float, longi: float):
    find_pin = db.query(models.Place).filter(models.Place.pin == pin).first()
    if find_pin:
        return find_pin

    return check_near(db=db, lati=lati, longi=longi)


def create_place(db: Session, plac: schemas.PlaceCreate):
    db_user = models.Place(pin=plac.pin, place_name=plac.place_name, parent_place=plac.parent_place,
                           latitude=plac.latitude, longitude=plac.longitude)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
