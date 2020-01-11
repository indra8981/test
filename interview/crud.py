from sqlalchemy.orm import Session

from . import schemas, models
from sqlalchemy import func
import math
import sqlalchemy
from sqlalchemy import tuple_


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


def get_places_by_distance_me(db: Session, lati: float, longi: float):
    all = db.query(models.Place.latitude, models.Place.longitude).all()
    all_points = distance_me(all, lati, longi, 5)
    return actual_places(db=db, all_points=all_points)
    # print(latt)
    # print(long)
    # return db.query(models.Place).filter(tuple_(models.Place.latitude,models.Place.longitude)._in(all_points))
    # return db.query(models.Place).filter(models.Place.latitude._in(latt), models.Place.longitude._in(long)).all()


def actual_places(db: Session, all_points):
    total = []
    for i in range(len(all_points)):
        now = db.query(models.Place).filter(models.Place.latitude == all_points[i][0],
                                            models.Place.longitude == all_points[i][1]).all()
        for place in now:
            total.append(place)
    return total


def get_places_by_distance_postgresql(db: Session, lati: float, longi: float):
    all = db.query(models.Place.latitude, models.Place.longitude).all()
    all_points = distance_postgre(all, lati, longi, 5000)
    return actual_places(db=db, all_points=all_points)


def distance_me(points, lati, longi, dist):
    all_point = []
    for i in range(len(points)):
        two_pair_distance = distance((lati, longi), (float(points[i][0]), float(points[i][1])))
        if (two_pair_distance <= dist):
            all_point.append((float(points[i][0]), float(points[i][1])))
    return all_point


# expr = func.is_equal("a", "b").as_comparison(1, 2)
def distance_postgre(points, lati, longi, dist):
    all_point = []
    # for i in range(len(points)):
    #     print(func.ll_to_earth(lati, longi))
    two_pair_distance = func.earth_distance(func.ll_to_earth(models.Place.latitude, models.Place.longitude),
                                            func.ll_to_earth(float(lati), float(longi)))
    # if (two_pair_distance <= dist):
    all_point.append(two_pair_distance <= dist)
    for i in all_point:
        print(i)
    print(all_point)
    return all_point


def get_place_by_latitude_longitude(db: Session, lati: float, longi: float):
    # print(db.query(models.Place).filter(models.Place.latitude == lati, models.Place.longitude == longi).all())
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
