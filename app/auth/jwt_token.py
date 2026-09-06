
from jose import jwt,JWTError
from datetime import timedelta,timezone,datetime
from config import settings
from fastapi import Depends,status,HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

OAuth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_access_token(username:str,id:int,role:str):
    encode = {'sub':username,'id':id,'role':role}
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME)
    encode.update({'exp':expires})
    return jwt.encode(encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

def get_current_user(token:Annotated[str,Depends(OAuth2_bearer)]):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        id = payload.get('id')
        role = payload.get('role')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')

        return {'username':username,'id':id,'role':role}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token')