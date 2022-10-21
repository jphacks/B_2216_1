from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import schemas
from .models import User, TimeData


async def get_user(db: AsyncSession, user_id: int):
    ret = await db.execute(select(User).filter(User.id == user_id))
    return ret.first()


async def get_user_by_shown_id(db: AsyncSession, shown_id: str):
    ret = await db.execute(select(User).filter(User.shown_id == shown_id))
    return ret.first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    ret = await db.execute(select(User).offset(skip).limit(limit))
    return ret.all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = User(shown_id=user.shown_id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# def get_sensors(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Sensor).offset(skip).limit(limit).all()

# def get_sensor(db: Session, sensor_id: int):
#     return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

# def create_user_sensor(db: Session, sensor: schemas.SensorCreate, user_id: int):
#     db_sensor = models.Sensor(**sensor.dict(), user_id=user_id)
#     db.add(db_sensor)
#     db.commit()
#     db.refresh(db_sensor)
#     return db_sensor


async def get_timedata(db: AsyncSession, sensor_id: int, skip: int = 0, limit: int = 100):
    ret = await db.execute(select(TimeData).filter(TimeData.id == sensor_id).offset(skip).limit(limit))
    return ret.all()

async def get_timedata_mean(db: AsyncSession, sensor_id: int, days: int, timestep: int, offset_day: int = 0):
    now = datetime.now() - timedelta(offset_day)

    ret = []
    for i in range(timestep, 0, -1):
        time = now - timedelta((1 - ((i - 1) / timestep)) * days)
        time_next = now - timedelta((1 - (i / timestep)) * days)
        datas = await db.execute(select(TimeData).filter(TimeData.id == sensor_id).filter(TimeData.timestamp > time).filter(TimeData.timestamp < time_next))
        mean: float = 0
        for data in datas.all():
            mean += data.value
        if len(datas) > 0:
            mean /= len(datas)
        ret.append(schemas.TimeData(id=sensor_id, timestamp=time, value=mean))
    return ret

async def get_sitting_time(db: AsyncSession, sensor_id: int, days: int, timestep: int, offset_day: int = 0, limit: float = 10) -> List[schemas.SittingData]:
    now = datetime.now() - timedelta(offset_day)
    time_per_step = days / timestep * 24

    ret = []
    for i in range(timestep, 0, -1):
        start = now - timedelta((1 - ((i - 1) / timestep)) * days)
        end = now - timedelta((1 - (i / timestep)) * days)
        query_all = select(TimeData).filter(TimeData.id == sensor_id).filter(TimeData.timestamp > start).filter(TimeData.timestamp < end)
        query_sitting = query_all.filter(TimeData.value > limit)
        datas_all_promise = db.execute(query_all)
        datas_sitting_promise = db.execute(query_sitting)
        datas_all = (await datas_all_promise).all()
        datas_sitting = (await datas_sitting_promise).all()
        hours: float = 0
        if len(datas_all) > 0:
            hours = time_per_step * (len(datas_sitting) / len(datas_all))
        ret.append(schemas.SittingData(start=start, end=end, hours=hours, id=sensor_id))
    return ret

async def create_timedata(db: AsyncSession, timedata: schemas.TimeDataCreate):
    now = datetime.now()
    db_timedata = TimeData(**timedata.dict(), timestamp=now)
    db.add(db_timedata)
    await db.commit()
    await db.refresh(db_timedata)
    return db_timedata
