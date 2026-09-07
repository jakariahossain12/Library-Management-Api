from fastapi import APIRouter,status,HTTPException,Query
from dependencies import user_dependency,db_dependency
from fastapi.responses import JSONResponse
from typing import Optional
from app.schemas.book import BookCreate,BookUpdate
from app.curd.admin import create_book,book_update


router = APIRouter(tags=['Admin'])



@router.post('/admin/create_book',status_code=status.HTTP_201_CREATED)
def create_new_book(user:user_dependency,db:db_dependency,new_book:BookCreate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")

    create_book(db,new_book)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content="new book create successfully")

@router.put('/admin/update_book/{book_id}',status_code=status.HTTP_200_OK)
def create_new_book(user:user_dependency,db:db_dependency,update_book:BookUpdate,book_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")

    book_update(db,update_book,book_id)
    return JSONResponse(status_code=status.HTTP_200_OK,content="Book update successfully")








