from fastapi import APIRouter,status,HTTPException,Query
from dependencies import user_dependency,db_dependency
from app.curd.book import get_all_books,get_specific_book
from fastapi.responses import JSONResponse
from typing import Optional


router = APIRouter(tags=['Get Books for users'])



@router.get('/books/all',status_code=status.HTTP_200_OK)
def get_All_Book(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    tran = get_all_books(db)
    return tran




@router.get('/books/{book_id}',status_code=status.HTTP_200_OK)
def get_Single_Book(user:user_dependency,db:db_dependency,book_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    tran = get_specific_book(db,book_id)
    return tran


