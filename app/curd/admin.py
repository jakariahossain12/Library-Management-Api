from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.Book import Book
from app.schemas.book import BookCreate,BookUpdate



def create_book(db:Session,new_book:BookCreate):
    book_model = Book(
        **new_book.model_dump(),
        available_copies = new_book.total_copies
    )
    db.add(book_model)
    db.commit()
    db.refresh(book_model)

def book_update(db:Session,update_book:BookUpdate,book_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

    update_data = update_book.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(book,key,value)
    db.commit()
    db.refresh(book)

def book_delete(db:Session,book_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

    db.query(Book).filter(Book.id == book_id).delete()

    db.commit()
    db.refresh()

