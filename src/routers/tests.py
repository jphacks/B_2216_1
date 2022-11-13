from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from typing import List

from .. import schemas, crud, timedata_handler

from ..dependencies.db import get_db

tests_router = APIRouter(redirect_slashes=False, tags=['test'])


@tests_router.get('/users/test/notify/{user_id}')
@tests_router.get('/users/test/notify/{user_id}/')
def notify_test(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="Call for non-exist user")

    delta = timedelta(hours=3)
    ok = timedata_handler.notify_rest(db, user_id, delta)

    if ok:
        return {'status': 200}
    else:
        raise HTTPException(status_code=404, detail="Unable to call APNs API")


@tests_router.get('/users/test/notify_posture/{user_id}')
@tests_router.get('/users/test/notify_posture/{user_id}/')
def notify_posture_test(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="Call for non-exist user")

    delta = timedelta(hours=3)
    ok = timedata_handler.notify_rest(db, user_id, delta)

    if ok:
        return {'status': 200}
    else:
        raise HTTPException(status_code=404, detail="Unable to call APNs API")
