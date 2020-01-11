from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from interview import schemas
from interview import crud, models
from interview.database import SessionLocal, engine

from numpy import genfromtxt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


load_file = False  # Make it true to load file to Database


def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, dtype=str)
    return data.tolist()


def loadfile(load_file):
    if (not load_file):
        return
    file_name = "IN.csv"
    data = Load_Data(file_name)
    sess = SessionLocal()
    for i in data:
        try:
            record = models.Place(**{

                'pin': i[0][3:],
                'place_name': i[1],
                'parent_place': i[2],
                'latitude': float(i[3]),
                'longitude': float(i[4]),
                'accuracy': int(i[5]) if i[5] != '' else 6
            })
            sess.add(record)
        except:
            continue
    sess.commit()
    sess.close()


loadfile(load_file)


@app.post("/post_location", response_model=schemas.Place)
def create_user(plac: schemas.PlaceCreate, db: Session = Depends(get_db)):
    db_user = crud.get_place_by_pin(db, pin=plac.pin, lati=plac.latitude, longi=plac.longitude)
    if db_user:
        raise HTTPException(status_code=400, detail="Place already Exists")
    return crud.create_place(db=db, plac=plac)


@app.get("/get_location/{latitude}&{longitude}", response_model=List[schemas.Place])
def read_user(latitude: float, longitude: float, db: Session = Depends(get_db)):
    db_user = crud.get_place_by_latitude_longitude(db, lati=latitude, longi=longitude)
    if len(db_user) == 0:
        raise HTTPException(status_code=404, detail="Place not Found")
    return db_user


@app.get("/get_using_self/{latitude}&{longitude}", response_model=List[schemas.Place])
def read_user(latitude: float, longitude: float, db: Session = Depends(get_db)):
    db_user = crud.get_places_by_distance_me(db, lati=latitude, longi=longitude)
    if len(db_user) == 0:
        raise HTTPException(status_code=404, detail="Place not Found")
    return db_user


@app.get("/get_using_postgres/{latitude}&{longitude}", response_model=List[schemas.Place])
def read_user(latitude: float, longitude: float, db: Session = Depends(get_db)):
    db_user = crud.get_places_by_distance_postgresql(db, lati=latitude, longi=longitude)
    if len(db_user) == 0:
        raise HTTPException(status_code=404, detail="Place not Found")
    return db_user
