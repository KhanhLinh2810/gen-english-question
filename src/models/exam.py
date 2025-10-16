# # models.py
# from sqlalchemy import Column, Integer, String, Text, DateTime, func
# from sqlalchemy.orm import relationship
# from src.models.base import BaseModel
#
#
# class Exam(BaseModel):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String(50), unique=True, nullable=False, index=True) # belong to user?
#     title = Column(String(100), nullable=False) # gửi lên default là exam_username_new_date
#     duration = Column(Integer, nullable=False)
#     num_question = Column(Integer, nullable=False)
#     notes = Column(Text, nullable=False)
#
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
#
#     questions = relationship(
#         "Question",
#         back_populates="user",
#         cascade="all, delete",
#         passive_deletes=True
#     )