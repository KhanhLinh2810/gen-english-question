# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Date, DateTime, func
from sqlalchemy.orm import relationship
from src.models.base import BaseModel
from datetime import datetime

class Question(BaseModel):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    context = Column(Text, nullable=False)
    description = Column(Text, nullable=True) # danh cho cau hoi doan van
    tags = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

    
    user = relationship("User", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete", passive_deletes=True)
    comments = relationship("Comment", back_populates="question", cascade="all, delete", passive_deletes=True)
    ratings = relationship("Rating", back_populates="question", cascade="all, delete", passive_deletes=True)
