from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_timedata(db: Session, sensor_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.TimeData).filter(models.TimeData.id == sensor_id).offset(skip).limit(limit).all()

def get_timedata_mean(db: Session, sensor_id: int, days: int, timestep: int, offset_day: int = 0):
    now = datetime.now() - timedelta(offset_day)

    ret = []
    for i in range(timestep, 0, -1):
        time = now - timedelta((1 - ((i - 1) / timestep)) * days)
        time_next = now - timedelta((1 - (i / timestep)) * days)
        datas = db.query(models.TimeData).filter(models.TimeData.id == sensor_id).filter(models.TimeData.timestamp > time).filter(models.TimeData.timestamp < time_next).all()
        mean: float = 0
        for data in datas:
            mean += data.value
        if len(datas) > 0:
            mean /= len(datas)
        ret.append(schemas.TimeData(id=sensor_id, timestamp=time, value=mean))
    return ret

def get_sitting_time(db: Session, sensor_id: int, days: int, timestep: int, offset_day: int = 0, limit: float = 10):
    now = datetime.now() - timedelta(offset_day)
    time_per_step = days / timestep * 24

    ret = []
    for i in range(timestep, 0, -1):
        start = now - timedelta((1 - ((i - 1) / timestep)) * days)
        end = now - timedelta((1 - (i / timestep)) * days)
        query = db.query(models.TimeData).filter(models.TimeData.id == sensor_id).filter(models.TimeData.timestamp > start).filter(models.TimeData.timestamp < end)
        datas_all = query.all()
        datas_sitting = query.filter(models.TimeData.value > limit).all()
        hours: float = 0
        if len(datas_all) > 0:
            hours = time_per_step * (len(datas_sitting) / len(datas_all))
        ret.append(schemas.SittingData(start=start, end=end, hours=hours, id=sensor_id))
    return ret

def create_timedata(db: Session, timedata: schemas.TimeDataCreate) -> List[schemas.SittingData]:
    now = datetime.now()
    db_timedata = models.TimeData(**timedata.dict(), timestamp=now)
    db.add(db_timedata)
    db.commit()
    db.refresh(db_timedata)
    return db_timedata
