from database import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func,ForeignKey
from datetime import datetime

class Reservations(Base):
    __tablename__ = "reservations"


    id = Column(Integer, primary_key=True)
    book_id = Column(Integer,ForeignKey('books.id'))
    user_id = Column(Integer,ForeignKey('users.id'))
    reservations_date = Column(DateTime, default=func.now(), nullable=False)
    status = Column(String,default="pending")