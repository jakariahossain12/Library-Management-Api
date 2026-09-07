from fastapi import APIRouter,status,HTTPException,Query
from dependencies import user_dependency,db_dependency
from fastapi.responses import JSONResponse
from typing import Optional
from app.schemas.book import BookCreate
from app.curd.admin import create_book


router = APIRouter(tags=['Admin'])



@router.post('/admin/create_book',status_code=status.HTTP_201_CREATED)
def create_new_book(user:user_dependency,db:db_dependency,new_book:BookCreate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")

    create_book(db,new_book)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content="new book create successfully")







