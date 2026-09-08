from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.Book import Book
from app.models.user import User
from app.models.reservations import Reservations
from app.schemas.book import BookCreate,BookUpdate,IssueBook
from app.models.issueRecords import IssueRecords
from datetime import datetime,timedelta
from config import settings

def calculate_fine(due_date:datetime,return_date:datetime):
    overdue_days = (return_date.date() - due_date.date()).days
    if overdue_days > 0:
        return round(overdue_days * settings.FINE_PER_DAY,2)
    else:
        return 0.0


# get all users
def get_all_user(db:Session):
    users = db.query(User).all()
    return users




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


def book_issue(db:Session,issue_request:IssueBook):
    book = db.query(Book).filter(Book.id == issue_request.book_id).first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

    member = db.query(User).filter(User.id == issue_request.user_id).first()

    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Member not found")

    if book.available_copies <=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No copies Available")

    loan_days = 14
    issue_date = datetime.now
    issue_model = IssueRecords(
        book_id = issue_request.book_id,     
        user_id = issue_request.user_id,
        issue_date = issue_date,
        due_date = issue_date + timedelta(days=loan_days),
        status = 'issued'
    )
    book.available_copies -=1
    reservation = db.query(Reservations).filter(
        Reservations.book_id == issue_request.book_id,
        Reservations.user_id == issue_request.user_id,
        Reservations.status == 'pending'
    ).first()

    if reservation is not None:
        reservation.status = 'approved'

    db.add(issue_model)
    db.commit()
    db.refresh(issue_model)




def return_book(db:Session,issue_id:int):
    issue = db.query(IssueRecords).filter(IssueRecords.id == issue_id).first()

    if issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Issue record not found")

    return_date = datetime.now
    fine = calculate_fine(issue.due_date,return_date)

    issue.return_date = return_date
    issue.status = 'returned'
    issue.fine_amount = fine


    book = db.query(Book).filter(Book.id == issue.book_id).first()
    if book is not None:
        book.available_copies +=1


    db.commit()
    db.refresh()
    return fine


def not_return_book(db:Session):
    not_return = db.query(IssueRecords).filter(IssueRecords.status != 'returned').all()
    return not_return



def fine_paid(db:Session,issue_id:int):
    issue = db.query(IssueRecords).filter(IssueRecords.id == issue_id).first()

    if issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Issue record not found")

    issue.fine_paid = True

