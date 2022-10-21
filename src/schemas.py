from datetime import datetime
from typing import List
from pydantic import BaseModel

class SensorBase(BaseModel):
    description: str

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    shown_id: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
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