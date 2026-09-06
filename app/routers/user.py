from fastapi import APIRouter,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import db_dependency,user_dependency
from app.schemas.user import UserUpdate,PasswordUpdate
from app.curd.user import update_user,password_change
from typing import Annotated
from app.schemas.user import UserCreate
from app.curd.user import crate_new_user,login_user,view_profile
from fastapi.responses import JSONResponse

router = APIRouter(tags=['users login'])

@router.post('/auth/register')
def sin_Up(db:db_dependency,new_user:UserCreate):
    user = crate_new_user(db,new_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content=user)

@router.post('/auth/login')
def login(db:db_dependency,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    token = login_user(db,form_data)
    return{
        'access_token':token,
        'token_type':'bearer'
    }


@router.get("/profile")
def view_Profile(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='failed Authentication') 
    user_data = view_profile(db,user.get('id'))
    return{'user':user_data}


@router.put('/edit-user')
def edit_user (user:user_dependency,db:db_dependency,update_User:UserUpdate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='failed Authentication') 

    update_user(db,user.get('id'),update_User)
    return JSONResponse(status_code=201,content={'message':'user update successfully'})

@router.patch('/change-password')
def change_password(user:user_dependency,db:db_dependency,update_pass:PasswordUpdate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='failed Authentication') 

    password_change(db,user.get('id'),update_pass)
    return JSONResponse(status_code=201,content={'message':'password update successfully'})
