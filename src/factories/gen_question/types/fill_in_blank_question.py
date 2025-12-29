from typing import List, Optional
import random

from src.enums import QuestionTypeEnum, ChoiceTypeEnum
from src.factories.gen_question.types.base import Question
from src.llms.models import GeminiLLM
from src.llms.tools import GEN_FILL_IN_BLANK_QUESTION_TOOL
from src.llms.prompts import GEN_FILL_IN_BLANK_QUESTION_PROMPT


class FillInBlankQuestion(Question):
    """
    This class generates multiple-choice 'fill in the blank' questions.

    It picks a word, generates a sentence containing it, replaces it with a blank,
    and provides several answer choices (one correct and others incorrect).
    """

    def generate_questions(self, list_words: List[str], num_question: int = 1, num_ans_per_question: int = 4):
        if not list_words:
            list_words = []

        list_unique_words = set(list_words)

        prompt = GEN_FILL_IN_BLANK_QUESTION_PROMPT
        _tools = [GEN_FILL_IN_BLANK_QUESTION_TOOL]
        raw_output = self.llm.generate_response(
             messages=[
                {
                    "role": "system",
                    "content": prompt
                }, 
                {
                    "role": "user",
                    "content": f"""
                        Please generate exactly {num_question} English questions.
                        - Keywords to use: {', '.join(list(list_unique_words))}
                        - Question type: {ChoiceTypeEnum.SINGLE_CHOICE.value}
                        - Choices per question: {num_ans_per_question}

                        You MUST call the 'gen_fill_in_blank_questions' tool with the FINAL CONTENT of the questions. 
                        Do not pass the requirements into the tool; pass the generated results.
                    """
                }
            ],
            tools=_tools,
        )
        
        return self._parse_raw_tool_output(
            raw_output=raw_output, 
            name_function="gen_fill_in_blank_questions", 
            type=QuestionTypeEnum.FILL_IN_BLANK
        )

