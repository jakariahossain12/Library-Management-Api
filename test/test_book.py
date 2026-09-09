from test.test_main import client
from database import SessionLocal
from main import app
from fastapi import status
from app.auth.jwt_token import get_current_user
from app.models.user import User
from app.models.Book import Book
from datetime import date

def overrides_ger_current_user():
    return{
        "id":1,
        'username':'testuser',
        'role':'librarian'
    }

def test_transactions():
    db = SessionLocal()

    
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(
                id=1,
                username="testuser",
                email="test@example.com",
                firstname = 'testuser',
                lastname = 'testuser',
                hashed_password="fake",
                role = "librarian"
            )
        db.add(user)
        db.commit()


    tran_data = db.query(Book).filter(Book.id == 555).first()

    if not tran_data:
        book = Book(
            id=555,
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            description="A novel about the American Dream in the 1920s.",
            price=15.99,
            total_copies=5,
            category="Fiction"
        )
        db.add(book)
        db.commit()



app.dependency_overrides[get_current_user] = overrides_ger_current_user

# get book ================================

def test_get_all_book():
    response = client.get('/books/all')
    assert response.status_code == status.HTTP_200_OK

def test_get_single_book():
    response = client.get('/books/555')
    assert response.status_code == status.HTTP_200_OK

# reservation  ==============================

def test_book_reservation():
    response = client.post('/reserve/555')
    assert response.status_code == status.HTTP_201_CREATED


def test_my_reservation():
    response = client.get('/my/reserve')
    assert response.status_code == status.HTTP_200_OK


def test_cancel_reservation():
    response = client.put('/reserve/cancel/1')
    assert response.status_code == status.HTTP_200_OK


def test_book_issueRecords():
    response = client.get('/my/issue_records')
    assert response.status_code == status.HTTP_200_OK

# admin router ==============================
def test_getAll_user():
    response = client.get('/admin/all_user')
    assert response.status_code == status.HTTP_200_OK


def test_getAll_user():
    response = client.get('/admin/all_not_return_book')
    assert response.status_code == status.HTTP_200_OK


def test_getAll_user():
    update_data = {
        "role":"librarian"
    }
    response = client.patch('/admin/role_update/1',json = update_data)
    assert response.status_code == status.HTTP_200_OK


def test_book_create():
    book_payload = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "A novel about the American Dream in the 1920s.",
    "price": 15.99,
    "total_copies": 5,
    "category": "Fiction"
}
    response = client.post('/admin/create_book',json = book_payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_book():
    update_data = {
        "title":"test update"
    }
    response = client.put('/admin/update_book/555',json = update_data)
    assert response.status_code == status.HTTP_200_OK

def test_book_issue():
    update_data = {
        "book_id":555,
        "user_id":1
    }
    response = client.post('/admin/create_issue',json = update_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_book_return():
    response = client.put('/admin/return_book/1')
    assert response.status_code == status.HTTP_200_OK


def test_fine_paid():
    response = client.patch('/admin/fine/pay/1')
    assert response.status_code == status.HTTP_200_OK


def test_book_delete():
    response = client.delete('/admin/delete_book/555')
    assert response.status_code == status.HTTP_200_OK

# my issue records =============================

def test_my_issue_records():
    response = client.get('/my/issue_records')
    assert response.status_code == status.HTTP_200_OK
