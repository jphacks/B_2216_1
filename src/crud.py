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


def create_user_sensor(db: Session, sensor: schemas.SensorCreate, user_id: int):
    db_sensor = models.Sensor(**sensor.dict(), user_id=user_id)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_timedata(db: Session, sensor_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.TimeData).filter(models.TimeData.sensor_id == sensor_id).offset(skip).limit(limit).all()


def create_sensor_timedata(db: Session, timedata: schemas.TimeData, sensor_id: int):
    db_timedata = models.TimeData(**timedata.dict(), sensor_id=sensor_id)
    db.add(db_timedata)
    db.commit()
    db.refresh(db_timedata)
    return db_timedata
