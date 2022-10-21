from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# class Sensor(Base):
#     __tablename__ = "sensors"

#     id = Column(Integer, primary_key=True, index=True)
#     description = Column(String, index=True)
#     datas = relationship("TimeData", back_populates="sensor")
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", back_populates="sensors")


class TimeData(Base):
    __tablename__ = "datas"

    data_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    # sensor_id = Column(Integer, ForeignKey("sensors.id"))
    id = Column(Integer, index=True)
    value = Column(Integer, index=True)
    # sensor = relationship("Sensor", back_populates="datas")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    shown_id = Column(String, index=True, unique=True)
    # sensors = relationship("Sensor", back_populates="user")
