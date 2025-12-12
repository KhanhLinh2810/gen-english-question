from typing import List, Optional
import random

from src.enums import QuestionTypeEnum
from src.factories.gen_question.types.base import Question
from src.llms.models import GeminiLLM
from src.llms.prompts import GEN_NATURAL_SENTENCE_PROMPT


class RearrangenQuestion(Question):
    """
    This class generates multiple-choice 'rearrange' questions.
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

            prompt = GEN_NATURAL_SENTENCE_PROMPT
            sentence = self.llm.generate_response(
                 messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }, 
                    {
                        "role": "user",
                        "content": f"List of words: {', '.join(list_choice_words)}"
                    }
                ],
            )

            choices = [{
                "content": sentence,
                "is_correct": True
            }]
            words = sentence.split()
            shuffled_words = words[:]
            random.shuffle(shuffled_words)
            question = " / ".join(shuffled_words)
            
            for i in range(num_ans_per_question-1):
                random.shuffle(shuffled_words)
                choices.append({
                    "content": " / ".join(shuffled_words),
                    "is_correct": False
                })

            result.append({
                "content": question, 
                "type": QuestionTypeEnum.REARRANGE,
                "choices": choices
            })
            
        return result