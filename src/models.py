from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    # description = Column(String, index=True)
    datas = relationship("TimeData", back_populates="sensor")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sensors")


class TimeData(Base):
    __tablename__ = "datas"

    data_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    # sensor_id = Column(Integer, ForeignKey("sensors.id"))
    id = Column(Integer, ForeignKey("sensors.id"), index=True)
    value = Column(Integer, index=True)
    sensor = relationship("Sensor", back_populates="datas")
    # sensor = relationship("Sensor", back_populates="datas")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String, index=True)
    # sensor_id = Column(Integer, ForeignKey("sensors.id"))
    sensors = relationship("Sensor", back_populates="user")

class ContinuousSitting(Base):
    __tablename__ = "c_sitting"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    last_stand = Column(DateTime, index=True)
    last_notify = Column(DateTime, index=True)