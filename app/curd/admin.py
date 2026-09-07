from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.Book import Book
from app.schemas.book import BookCreate



def create_book(db:Session,new_book:BookCreate):
    book_model = Book(
        **new_book.model_dump(),
        available_copies = new_book.total_copies
    )
    db.add(book_model)
    db.commit()
    db.refresh(book_model)

