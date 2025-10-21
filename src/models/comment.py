# models.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Comment(BaseModel):
    """
    Represents a comment made by a user on a question.
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="comments")
    question = relationship("Question", back_populates="comments")

    def __repr__(self):
        return f"<Comment id={self.id}, user_id={self.user_id}, question_id={self.question_id}, content_id={self.content}>"
