from app.schemas.user import UserCreate,UserUpdate,PasswordUpdate
from sqlalchemy.orm import Session
import bcrypt
from fastapi import HTTPException,status
from passlib.context import CryptContext
from app.models.user import User 

from app.auth.jwt_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
bcrypt.__about__ = bcrypt

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_user_by_username(db:Session,username:str):
    return db.query(User).filter(User.username == username).first()

def crate_new_user(db:Session,new_user:UserCreate):
    db_user = User(
        username = new_user.username,
        email = new_user.email,
        hashed_password = pwd_context.hash(new_user.password),
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        role = new_user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user = {
        "id" : db_user.id,
        "username" : db_user.username,
        "email" : db_user.email,
        "firstname":db_user.firstname,
        "lastname":db_user.lastname,
        "role":db_user.role
    }
    return user

def login_user(db:Session,form_data:OAuth2PasswordRequestForm):
    user = db.query(User).filter(User.username == form_data.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')

    if pwd_context.verify(form_data.password,user.hashed_password):
        token = create_access_token(user.username,user.id,user.role)
        return token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='password did not match')


def view_profile(db:Session,user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def password_change(db:Session,user_id:int,updatePass:PasswordUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
            raise HTTPException(status_code=404,detail="user not found")

    if pwd_context.verify(updatePass.old_password, user.hashed_password):
        user.hashed_password = pwd_context.hash(updatePass.new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="password did not match")


def update_user(db:Session,user_id : int, updateUser:UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    
    update_data = updateUser.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(user,key,value)
    
    db.commit()