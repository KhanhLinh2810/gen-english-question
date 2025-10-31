import random

from src.enums import QuestionTypeEnum
from src.interfaces.question import ICreateQuestionForParagraph
from src.factories.gen_question_for_paragraph.types.base import Question
from src.llms.models import GeminiLLM


class ParagraphQuestion(Question):
    def __init__(self):
        self.llm = GeminiLLM()

    def generate_questions(self, data: ICreateQuestionForParagraph):
        