from database import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func
from datetime import datetime

class Book(Base):
    __tablename__ = "books"


    id = Column(Integer, primary_key=True)
    
    
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    
    
    description = Column(Text, nullable=True) 
    
    price = Column(Float, default=0.0, nullable=False)
    total_copies = Column(Integer, default=5, nullable=False)
    available_copies = Column(Integer, default=5, nullable=False)
    
    cover_image = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)