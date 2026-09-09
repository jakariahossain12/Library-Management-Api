from fastapi import APIRouter,status,HTTPException,Query
from dependencies import user_dependency,db_dependency
from fastapi.responses import JSONResponse
from typing import Optional,List
from pydantic import BaseModel
from app.schemas.user import UserResponse,RoleUpdate
from app.schemas.book import BookCreate,BookUpdate,IssueBook
from app.curd.admin import create_book,book_update,book_delete,book_issue,return_book,fine_paid,get_all_user,not_return_book,role_update


router = APIRouter(tags=['Admin'])

class UserListResponse(BaseModel):
    users: List[UserResponse]

@router.get('/admin/all_user/',status_code=status.HTTP_200_OK,response_model=UserListResponse)
def get_All_User(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    users = get_all_user(db)
    return {"users":users}

@router.get('/admin/all_not_return_book/',status_code=status.HTTP_200_OK)
def not_return_Book(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    not_return = not_return_book(db)
    return {"Not_return_book":not_return}

@router.patch('/admin/role_update/{user_id}', status_code=status.HTTP_200_OK)
def user_role_update(
    user: user_dependency, 
    db: db_dependency, 
    user_id: int, 
    update_role: RoleUpdate
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed authentication")
    if str(user.get('role')) != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden access")

    role_update(db, user_id, update_role)
    return {"message": "User role updated successfully"}

@router.post('/admin/create_book',status_code=status.HTTP_201_CREATED)
def create_new_book(user:user_dependency,db:db_dependency,new_book:BookCreate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    create_book(db,new_book)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content="new book create successfully")





@router.put('/admin/update_book/{book_id}',status_code=status.HTTP_200_OK)
def update_book(user:user_dependency,db:db_dependency,update_book:BookUpdate,book_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    book_update(db,update_book,book_id)
    return JSONResponse(status_code=status.HTTP_200_OK,content="Book update successfully")





@router.delete('/admin/delete_book/{book_id}',status_code=status.HTTP_200_OK)
def delete_book(user:user_dependency,db:db_dependency,book_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    book_delete(db,book_id)
    return JSONResponse(status_code=status.HTTP_200_OK,content="Book delete successfully")



@router.post('/admin/create_issue/',status_code=status.HTTP_201_CREATED)
def create_issue(user:user_dependency,db:db_dependency,issue_request:IssueBook):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    book_issue(db,issue_request)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content="Book issued successfully")



@router.put('/admin/return_book/{issue_id}',status_code=status.HTTP_200_OK)
def book_return(user:user_dependency,db:db_dependency,issue_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    fine = return_book(db,issue_id)
    return JSONResponse(status_code=status.HTTP_200_OK,content={'message':"Book returned successfully","fine_amount":fine})


@router.patch('/admin/fine/pay/{issue_id}',status_code=status.HTTP_200_OK)
def fine_Paid(user:user_dependency,db:db_dependency,issue_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed Authentication")
    if user.get('role') != 'librarian':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden access")

    fine_paid(db,issue_id)
    return JSONResponse(status_code=status.HTTP_200_OK,content={'message':"Fine paid successfully"})









