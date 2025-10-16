# # models.py
# from sqlalchemy import Column, Integer, String, Text, DateTime, func
# from sqlalchemy.orm import relationship
# from src.models.base import BaseModel
#
#
# class ExamQuestion(BaseModel):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     question_id = Column(String(50), unique=True, nullable=False, index=True) # nguoi thi
#     exam_id = Column(String(50), unique=True, nullable=False, index=True) # nguoi thi
#     score = Column(Integer, nullable=False)
#
#     questions = relationship(
#         "Question",
#         back_populates="user",
#         cascade="all, delete",
#         passive_deletes=True
#     )