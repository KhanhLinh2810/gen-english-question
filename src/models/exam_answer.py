# models.py
from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class ExamAttempt(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String(50), unique=True, nullable=False, index=True) # nguoi thi
    exam_attempt_id = Column(String(50), unique=True, nullable=False, index=True) # nguoi thi
    is_selected = Column(Boolean, nullable=False, default=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    questions = relationship(
        "Question",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )