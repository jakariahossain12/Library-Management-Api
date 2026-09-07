import datetime
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: Annotated[str, Field(..., description="Title of the Book")]
    author: Annotated[str, Field(..., description="Author of the Book")]
    description: Annotated[str, Field(default='',max_length=200, description="Description of the Book")]
    price:Annotated[float,Field(default=0.0,ge=0,description='price of the book')]
    total_copies:Annotated[int,Field(default=1,description="Total copies of the book")]
    category: Annotated[str, Field(..., description="Category")]
    


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    author: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    category: Optional[str] = Field(default=None)
    total_copies: Optional[str] = Field(default=None)
    available_copies: Optional[str] = Field(default=None)


