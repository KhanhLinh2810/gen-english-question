from abc import ABC, abstractmethod
from typing import Set

import nltk

nltk.download('words')
from nltk.corpus import words

nltk_words = words.words()

class Question(ABC):
    @abstractmethod
    def generate_questions(self, words: Set[str], num_questions: int = 1, num_ans_per_question: int = 4):
        pass

    @staticmethod
    def cal_num_word_in_list_available_per_question(
            len_list_words: int,
            num_questions: int = 1,
            num_ans_per_question: int = 4
    ) -> int:
        return min(len_list_words//num_questions, num_ans_per_question)