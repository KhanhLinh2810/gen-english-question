# # models.py
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Float, func
# from sqlalchemy.orm import relationship
# from src.models.base import BaseModel
# from datetime import datetime

# class Question(BaseModel):
#     __tablename__ = "questions"
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     content = Column(Text, nullable=False)
#     description = Column(Text, nullable=True)  # Dành cho câu hỏi dạng đoạn văn
#     tags = Column(Text, nullable=True)
#     score = Column(Float, nullable=True, default=1.0)
#     list_choice_id = Column(Text, nullable=True, comment='JSON array: ["1","2","3","4"]')
#     list_comment_id = Column(Text, nullable=True, comment='JSON array: ["12","15","22"]')
#     list_rating_id = Column(Text, nullable=True, comment='JSON array: ["8","10"]')

#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

#     # Relationships
#     user = relationship("User", back_populates="questions")
#     choices = relationship("Choice", back_populates="question", cascade="all, delete", passive_deletes=True)
#     comments = relationship("Comment", back_populates="question", cascade="all, delete", passive_deletes=True)
#     ratings = relationship("Rating", back_populates="question", cascade="all, delete", passive_deletes=True)

#     def __repr__(self):
#         return f"<Question id={self.id} user_id={self.user_id} score={self.score}>"
