# # models.py
# from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
# from sqlalchemy.orm import relationship
# from src.models.base import BaseModel

# class Rating(BaseModel):
#     __tablename__ = "ratings"
    
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
#     question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
#     rating_value = Column(Integer, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())  
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

#     question = relationship("Question", back_populates="ratings")