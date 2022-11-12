from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from typing import List

from .. import schemas, crud, timedata_handler

from ..dependencies.db import get_db


users_router = APIRouter(redirect_slashes=False, tags=['users', 'sensors'])

# post user


@users_router.post("/users", response_model=schemas.User)
@users_router.post("/users/", response_model=schemas.User)
def create_user_and_sensor(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.id)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"User #{user.id} is already registered")
    user = crud.create_user(db=db, user=user)
    sensor = schemas.SensorCreate(id=user.id, user_id=user.id)
    crud.create_sensor(db=db, sensor=sensor)
    return user


@users_router.get("/users", response_model=List[schemas.User])
@users_router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/users/{user_id}", response_model=schemas.User)
@users_router.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.get('/users/test/notify/{user_id}')
def notify_test(user_id: int, db: Session = Depends(get_db)):
    delta = timedelta(hours=3)
    ok = timedata_handler.notify(db, user_id, delta)

    if ok:
        return {'status': 200}
    else:
        raise HTTPException(status_code=404, detail="Unable to call APNs API")
