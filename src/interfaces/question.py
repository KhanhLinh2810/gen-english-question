from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from src.enums import QuestionTypeEnum


class ModelInput(BaseModel):
    """General request model structure for flutter incoming req."""
    user_id: Optional[str] = None
    context: str
    name: str

class ICQuestion(BaseModel):
    context: str
    name: str

class ICreateQuestion(BaseModel):
    question_type: QuestionTypeEnum
    list_words: List[str]
    num_ans_per_question: int = Field(..., ge=2, le=10)
    num_question: int = Field(..., ge=1, le=10)

    @field_validator('list_words')
    def check_single_word(cls, value):
        for word in value:
            if " " in word:
                raise ValueError("list_words_just_includes_single_word")
        return value
