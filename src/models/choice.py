# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Choice(BaseModel):
    """
    Represents a single answer choice for a question.
    """
    __tablename__ = "choices"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    explanation = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())  
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

    # Relationships
    question = relationship("Question", back_populates="choices")
    
    def __repr__(self):
        return f"<Choice id={self.id}, question_id={self.question_id}, is_correct={self.is_correct}>"