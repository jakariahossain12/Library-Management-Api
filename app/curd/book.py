from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.Book import Book



def get_all_books(db:Session):
    books = db.query(Book).all()
    return books

def get_specific_book(db:Session,book_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    return book



