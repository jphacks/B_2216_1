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
    sensor_id: int
    value: int
    timestamp: int

class TimeDataCreate(TimeDataBase):
    pass

class TimeData(TimeDataBase):
    sensor_id: int
    class Config:
        orm_mode = True