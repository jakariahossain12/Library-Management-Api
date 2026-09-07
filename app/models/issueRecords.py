from database import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func,ForeignKey,Boolean
from datetime import datetime

class IssueRecords(Base):
    __tablename__ = "issue_records"


    id = Column(Integer, primary_key=True,index=True)
    book_id = Column(Integer,ForeignKey('books.id'))
    user_id = Column(Integer,ForeignKey('users.id'))
    issue_date = Column(DateTime, default=func.now(), nullable=False)
    due_date = Column(DateTime)
    return_date = Column(DateTime,nullable=True)
    status = Column(String,default="issued") # issued or returned
    fine_amount = Column(Float,default=0.0)
    fine_paid = Column(Boolean,default=False)