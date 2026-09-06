from sqlalchemy.orm import sessionmaker,session
from sqlalchemy import create_engine
from config import settings
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Annotated

engine = create_engine(settings.DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)

Base = declarative_base()

