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
    def __init__(self):
        self.llm = GeminiLLM()

    def generate_questions(self, list_words: List[str], num_question: int = 1, num_ans_per_question: int = 4):
        if not list_words:
            list_words = []

        result = []
        list_unique_words = set(list_words)

        def choice_word_to_gen_sentence():
            number_choice_word = random.randint(1, 4)

            available_words = list(list_unique_words)
            if number_choice_word <= len(available_words):
                choice_word = random.sample(available_words, number_choice_word)
                for w in choice_word:
                    list_unique_words.remove(w)
                return choice_word
            return []

        for _ in range(num_question):
            list_choice_words = choice_word_to_gen_sentence()

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
                        "content": f"List of words: {', '.join(list_choice_words)}, Type of question: {ChoiceTypeEnum.SINGLE_CHOICE.value}, Number of answer choices: {num_ans_per_question}"
                    }
                ],
                tools=_tools,
            )
            
            if "tool_calls" in raw_output and raw_output["tool_calls"]:
                for call in raw_output["tool_calls"]:
                    if call.get("name") == "gen_fill_in_blank_question":
                        data = call.get("arguments", {})
                        result.append({
                            "question": data.get("question"),
                            "type": QuestionTypeEnum.FILL_IN_BLANK,
                            "choices": data.get("choices", []),
                            "answer": data.get("answer"),
                            "explanation": data.get("explanation"),
                            "tags": data.get("tags", []),
                        })

        return result