from datetime import datetime, timedelta
from pyexpat import model
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_shown_id(db: Session, shown_id: str):
    return db.query(models.User).filter(models.User.shown_id == shown_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(shown_id=user.shown_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

def create_user_sensor(db: Session, sensor: schemas.SensorCreate, user_id: int):
    db_sensor = models.Sensor(**sensor.dict(), user_id=user_id)
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
        mean = 0
        for data in datas:
            mean += data.value
        if len(datas) > 0:
            mean /= len(datas)
        ret.append(schemas.TimeData(id=sensor_id, timestamp=time, value=mean))
    return ret

def create_timedata(db: Session, timedata: schemas.TimeDataCreate):
    now = datetime.now()
    db_timedata = models.TimeData(**timedata.dict(), timestamp=now)
    db.add(db_timedata)
    db.commit()
    db.refresh(db_timedata)
    return db_timedata
