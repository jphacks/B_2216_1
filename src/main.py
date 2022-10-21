from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_session

import asyncio

from . import crud, models, schemas
from .database import engine

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(init_models())


app = FastAPI()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    async with async_session() as db:
        db_user = await crud.get_user_by_shown_id(db, shown_id=user.shown_id)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100):
    async with async_session() as db:
        users = await crud.get_users(db, skip=skip, limit=limit)
        return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int):
    async with async_session() as db:
        db_user = await crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

@app.get("/data/today/{sensor_id}", response_model=List[schemas.TimeData])
async def get_today_data(sensor_id):
    async with async_session() as db:
        ret = await crud.get_timedata(db, sensor_id=sensor_id, limit=24)
        if ret == None:
            raise HTTPException(status_code=404, detail="Sensor ID not found")
        return ret

@app.get("/data/mean/today/{sensor_id}", response_model=List[schemas.TimeData])
async def get_means_day(sensor_id: int):
    async with async_session() as db:
        return await crud.get_timedata_mean(db, sensor_id=sensor_id, days=1, timestep=24, offset_day=0)

@app.get("/data/mean/week/{sensor_id}", response_model=List[schemas.TimeData])
async def get_means_week(sensor_id: int):
    async with async_session() as db:
        return await crud.get_timedata_mean(db, sensor_id=sensor_id, days=7, timestep=7, offset_day=0)

@app.post("/data/", response_model=schemas.TimeData)
async def push_data(data: schemas.TimeDataPost):
    async with async_session() as db:
        value = data.w0 + data.w1 + data.w2 + data.w3
        timedata = schemas.TimeDataCreate(**data.dict(), value=value)
        ret = await crud.create_timedata(db, timedata=timedata)
        if ret == None:
            raise HTTPException(status_code=404, detail="Sensor ID not found")
        return ret

@app.get("/data/sitting/today/{sensor_id}", response_model=List[schemas.SittingData])
async def get_sitting_time_day(sensor_id: int):
    async with async_session() as db:
        return crud.get_sitting_time(db, sensor_id=sensor_id, days=1, timestep=24)
