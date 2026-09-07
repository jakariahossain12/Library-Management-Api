
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated,Optional
import enum


class UserRole(str, enum.Enum):
    LIBRARIAN = "librarian"
    MEMBER = "member"


class UserCreate(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=50, description="Unique username of the user")]
    email: Annotated[str, Field(..., description="User email address")]
    firstname: Annotated[str, Field(..., min_length=1, max_length=100, description="User first name")]
    lastname: Annotated[str, Field(..., min_length=1, max_length=100, description="User last name")]
    password: Annotated[str, Field(..., min_length=6, max_length=128, description="Password of the user")]
    role: Annotated[UserRole, Field(default=UserRole.MEMBER, description="User role (librarian or member)")]

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)

class PasswordUpdate(BaseModel):
    old_password:Annotated[str,Field(...,description="Enter your old password")]
    new_password:Annotated[str,Field(...,description="Enter your new password")]