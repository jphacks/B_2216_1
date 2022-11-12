from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from typing import List

import sys, os
sys.path.append(os.pardir)
from .. import schemas, crud

from ..dependencies.db import get_db

datas_router = APIRouter(redirect_slashes=False, tags=['datas'])

@datas_router.get("/data/today/{sensor_id}", response_model=List[schemas.TimeData])
@datas_router.get("/data/today/{sensor_id}/", response_model=List[schemas.TimeData])
def get_today_data(sensor_id, db: Session = Depends(get_db)):
    ret = crud.get_timedata(db, sensor_id=sensor_id, limit=24)
    if ret == None:
        raise HTTPException(status_code=404, detail="Sensor ID not found")
    return ret

@datas_router.get("/data/weight/today/{sensor_id}", response_model=List[schemas.TimeData])
@datas_router.get("/data/weight/today/{sensor_id}/", response_model=List[schemas.TimeData])
def get_means_day(sensor_id: int, db: Session = Depends(get_db)):
    return crud.get_timedata_mean(db, sensor_id=sensor_id, days=1, timestep=24, offset_day=0)

@datas_router.get("/data/weight/week/{sensor_id}", response_model=List[schemas.TimeData])
@datas_router.get("/data/weight/week/{sensor_id}/", response_model=List[schemas.TimeData])
def get_means_week(sensor_id: int, db: Session = Depends(get_db)):
    return crud.get_timedata_mean(db, sensor_id=sensor_id, days=7, timestep=7, offset_day=0)

@datas_router.get("/data/weight/month/{sensor_id}", response_model=List[schemas.TimeData])
@datas_router.get("/data/weight/month/{sensor_id}/", response_model=List[schemas.TimeData])
def get_means_month(sensor_id: int, db: Session = Depends(get_db)):
    return crud.get_timedata_mean(db, sensor_id=sensor_id, days=30, timestep=30, offset_day=0)

@datas_router.post("/data", response_model=schemas.TimeData)
@datas_router.post("/data/", response_model=schemas.TimeData)
def push_data(data: schemas.TimeDataPost, db: Session = Depends(get_db)):
    value = data.w0 + data.w1 + data.w2 + data.w3
    timedata = schemas.TimeDataCreate(**data.dict(), value=value)
    ret = crud.create_timedata(db, timedata=timedata)
    if ret == None:
        raise HTTPException(status_code=404, detail="Sensor ID not found")
    return ret

@datas_router.get("/data/sitting/today/{sensor_id}", response_model=List[schemas.SittingData])
@datas_router.get("/data/sitting/today/{sensor_id}/", response_model=List[schemas.SittingData])
def get_sitting_time_day(sensor_id: int, db: Session = Depends(get_db)):
    return crud.get_sitting_time(db, sensor_id=sensor_id, days=1, timestep=24)

@datas_router.get("/data/sitting/week/{sensor_id}", response_model=List[schemas.TimeData])
@datas_router.get("/data/sitting/week/{sensor_id}/", response_model=List[schemas.TimeData])
def get_sitting_week(sensor_id: int, db: Session = Depends(get_db)):
    return crud.get_timedata_mean(db, sensor_id=sensor_id, days=7, timestep=7, offset_day=0)

@datas_router.get("/data/sitting/month/{sensor_id}", response_model=List[schemas.TimeData])
@datas_router.get("/data/sitting/month/{sensor_id}/", response_model=List[schemas.TimeData])
def get_sitting_month(sensor_id: int, db: Session = Depends(get_db)):
    return crud.get_timedata_mean(db, sensor_id=sensor_id, days=30, timestep=30, offset_day=0)
