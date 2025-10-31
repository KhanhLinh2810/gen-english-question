from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Text

from src.enums import QuestionTypeEnum, ParagraphQuestionTypeEnum


class ModelInput(BaseModel):
    """General request model structure for flutter incoming req."""
    user_id: Optional[str] = None
    context: str
    name: str
    
class IQuestionConfig(BaseModel):
    question_type: QuestionTypeEnum
    list_words: List[str]
    num_question: int = Field(..., ge=1, le=5)

class ICreateQuestionForParagraph(BaseModel):
    description: Text
    num_ans_per_question: int = Field(..., ge=2, le=6)
    list_create_question: List[IQuestionConfig]

class ICreateQuestion(BaseModel):
    question_type: ParagraphQuestionTypeEnum
    list_words: List[str]
    num_ans_per_question: int = Field(..., ge=2, le=10)
    num_question: int = Field(..., ge=1, le=10)

    @field_validator('list_words')
    def check_single_word(cls, value):
        for word in value:
            if " " in word:
                raise ValueError("list_words_just_includes_single_word")
        return value
