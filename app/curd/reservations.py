from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.Book import Book
from app.models.reservations import Reservations




def reserve_book (db:Session,book_id:int,user_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

    reservation_model = Reservations(
        book_id = book_id,
        user_id = user_id,
        status = 'pending'
    )

    db.add(reservation_model)
    db.commit()
    db.refresh(reservation_model)


def cancel_reserve_book (db:Session,reservations_id:int):
    reservation = db.query(Reservations).filter(Reservations.id == reservations_id).first()
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Reservation not found")

    reservation.status = 'cancelled'

    db.commit()
    db.refresh(reservation)


def my_reservation (db:Session,user_id:int):
    reservations = db.query(Reservations).filter(Reservations.user_id == user_id).all()
    return reservations

