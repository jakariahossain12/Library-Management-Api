from fastapi import APIRouter,status,HTTPException,Query
from dependencies import user_dependency,db_dependency
from app.curd.reservations import reserve_book,cancel_reserve_book,my_reservation,my_issueRecords
from fastapi.responses import JSONResponse
from typing import Optional


router = APIRouter(tags=[' Books reservation for users'])





@router.post('/reserve/{book_id}',status_code=status.HTTP_201_CREATED)
def book_reservation(user:user_dependency,db:db_dependency,book_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    reserve_book(db,book_id,user.get('id'))
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'message':'Book reserve successfully'})



@router.get('/my/reserve',status_code=status.HTTP_200_OK)
def book_reservation(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    res = my_reservation(db,user.get('id'))
    return res

@router.get('/my/issue_records',status_code=status.HTTP_200_OK)
def book_issueRecords(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    res = my_issueRecords(db,user.get('id'))
    return res



@router.put('/reserve/cancel/{reservation_id}',status_code=status.HTTP_200_OK)
def book_reservation_cancel(user:user_dependency,db:db_dependency,reservation_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    cancel_reserve_book(db,reservation_id)
    return JSONResponse(content={'message':'Book Reservation cancel successfully'})



