import datetime
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field


class CreateTransaction(BaseModel):
    id: Annotated[int, Field(..., description="Unique ID for transaction")]
    title: Annotated[str, Field(..., description="Title of transaction")]
    amount: Annotated[float, Field(..., gt=0, description="Amount")]
    type: Annotated[
        Literal["income", "expense"], Field(..., description="Type")
    ]
    category: Annotated[str, Field(..., description="Category")]
    date: Annotated[
        datetime.date, Field(..., description="Date of transaction")
    ]


class UpdateTransaction(BaseModel):
    title: Optional[str] = Field(default=None)
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[Literal["income", "expense"]] = Field(default=None)
    category: Optional[str] = Field(default=None)
    date: Optional[datetime.date] = Field(default=None)