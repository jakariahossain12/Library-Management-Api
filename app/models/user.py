from database import Base
from sqlalchemy import Column,String,Integer,Float,Boolean,Enum
import enum

class UserRole(str,enum.Enum):
    LIBRARIAN = "librarian"
    MEMBER = "member"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),index=True,unique=True,nullable=False)
    email = Column(String(255),index=True, unique=True,nullable=False)
    hashed_password = Column(String(255),nullable=False)
    firstname = Column(String(255),nullable=False)
    lastname = Column(String(255),nullable=False)
    is_active = Column(Boolean,default=True)
    role = Column(Enum(UserRole),default=UserRole.MEMBER,nullable=False) # librarian or member
