from datetime import datetime
from typing import List
from pydantic import BaseModel

class SensorBase(BaseModel):
    id: int
    user_id: int

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: int              # corresponds with sensor id

class UserCreate(UserBase):
    device_token: str    # used when calling APNs API
    pass

class User(UserBase):
    sensors: List[Sensor] = []

    class Config:
        orm_mode = True

class TimeDataBase(BaseModel):
    id: int

class TimeDataPost(TimeDataBase):
    w0: float
    w1: float
    w2: float
    w3: float

class TimeDataCreate(TimeDataBase):
    value: float

class TimeData(TimeDataBase):
    timestamp: datetime
    value: float
    class Config:
        orm_mode = True

class SittingData(BaseModel):
    id: int
    start: datetime
    end: datetime
    hours: float