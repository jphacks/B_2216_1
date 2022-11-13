from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .routers.users import users_router
from .routers.datas import datas_router
from .routers.tests import tests_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(datas_router)
app.include_router(tests_router)
