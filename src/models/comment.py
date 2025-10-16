# models.py
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func, String
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Comment(BaseModel):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

    question = relationship("Question", back_populates="comments")
