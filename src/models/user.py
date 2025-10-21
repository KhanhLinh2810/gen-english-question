from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class User(BaseModel):
    """
    Represents an application user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    avatar_url = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    questions = relationship(
        "Question",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    ratings = relationship(
        "Rating",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    exam_attempts = relationship(
        "ExamAttempt",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    exams = relationship(
        "Exam",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<User id={self.id}, username='{self.username}', email='{self.email}'>"