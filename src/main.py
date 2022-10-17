import argparse
import random
import uvicorn
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_shown_id(db, shown_id=user.shown_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/data/{sensor_id}/today", response_model=List[schemas.TimeData])
def get_today_data(sensor_id, db: Session = Depends(get_db)):
    ret = crud.get_timedata(db, sensor_id=sensor_id, limit=24)
    if ret == None:
        raise HTTPException(status_code=404, detail="Sensor ID not found")
    return ret

@app.post("/data/", response_model=schemas.TimeData)
def push_data(data: schemas.TimeDataCreate, db: Session = Depends(get_db)):
    ret = crud.create_timedata(db, timedata=data)
    if ret == None:
        raise HTTPException(status_code=404, detail="Sensor ID not found")
    return ret

# @app.post("/sensors/", response_model=schemas.Sensor)
# def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
#     db_sensor = crud.create_user_sensor(db, sensor, )

# @app.get("/sensors/{sensor_id}", response_model=schemas.Sensor)
# def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
#     db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
#     if db_sensor is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_sensor


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
