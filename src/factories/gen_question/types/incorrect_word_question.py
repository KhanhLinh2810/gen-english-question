from typing import List, Optional
import random

from src.enums import ChoiceTypeEnum, QuestionTypeEnum
from src.factories.gen_question.types.base import Question
from src.llms.models import GeminiLLM
from src.llms.tools import GEN_INCORRECT_WORD_QUESTION_TOOL
from src.llms.prompts import GEN_INCORRECT_WORD_QUESTION_PROMPT

class IncorrectWordQuestion(Question):    
    def generate_questions(self, list_words: List[str], num_question: int = 1, num_ans_per_question: int = 4):
        if list_words is None:
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

            prompt = GEN_INCORRECT_WORD_QUESTION_PROMPT
            _tools = [GEN_INCORRECT_WORD_QUESTION_TOOL]
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
                    if call.get("name") == "gen_find_error_question":
                        data = call.get("arguments", {})
                        raw_choices = data.get("choices", [])
                        answer = data.get("answer")
                        if not raw_choices or not answer or answer not in raw_choices:
                            continue
                        choices = []
                        for c in raw_choices:
                            choices.append({
                                "content": c,
                                "is_correct": c == answer
                            })

                        result.append({
                            "content": data.get("question"),
                            "type": QuestionTypeEnum.INCORRECT_WORD,
                            "choices": choices, 
                            "explanation": data.get("explanation"),
                            "tags": data.get("tags", []),
                        })


            # random.shuffle(choices)
            # result.append({
            #     "question": modified_sentence,
            #     "type": QuestionTypeEnum.INCORRECT_WORD,
            #     "choices": choices,
            #     "answer": choices.index(incorrect_word),
            #     "explain": ["Correct: {sequence}"],
            # })

        return result