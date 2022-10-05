
from mysqlx import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "mysql+mysqlconnector://root:jphacks@localhost/test"

DECLARATIVE_BASE = declarative_base()

# engine生成
engine = create_engine(
    DATABASE_URI,
    encoding="utf-8",
    echo=True,
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
