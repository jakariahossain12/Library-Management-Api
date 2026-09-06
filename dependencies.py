from database import SessionLocal
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.auth.jwt_token import get_current_user

user_dependency = Annotated[dict,Depends(get_current_user)]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
