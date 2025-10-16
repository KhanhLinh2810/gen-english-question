# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Choice(BaseModel):
    __tablename__ = "choices"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    context = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    explanation = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())  
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

    question = relationship("Question", back_populates="choices")
