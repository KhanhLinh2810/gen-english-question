# # models.py
# from sqlalchemy import Column, Integer, String, Text, DateTime, func
# from sqlalchemy.orm import relationship
# from src.models.base import BaseModel
#
#
# class ExamAttempt(BaseModel):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String(50), unique=True, nullable=False, index=True) # nguoi thi
#     exam_id = Column(String(50), unique=True, nullable=False, index=True) # nguoi thi
#     started_at = Column(DateTime(timezone=True), server_default=func.now())
#     submitted_at = Column(DateTime(timezone=True), server_default=func.now())
#     score = Column(Integer, nullable=False)
#
#     questions = relationship(
#         "Question",
#         back_populates="user",
#         cascade="all, delete",
#         passive_deletes=True
#     )