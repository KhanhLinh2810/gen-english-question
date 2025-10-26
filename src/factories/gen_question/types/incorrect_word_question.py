from typing import List, Optional
import random

from src.enum import QuestionTypeEnum
from src.enum import TransformWordType
from src.factories.gen_question.types.base import Question, nltk_words
from src.factories.transform_word.factory import transform_word_instance
from src.services.AI.sentence_generator import SentenceGeneratorModel


class IncorrectWordQuestion(Question):
    """
    This class generates multiple-choice questions that ask the user
    to find the incorrect word in a sentence.

    It selects a word from the list, generates a sentence using a simple pattern,
    and injects a grammatically incorrect word into the sentence.
    """

    def generate_questions(self, list_words: List[str], num_question: int = 1, num_ans_per_question: int = 4):
        if list_words is None:
            list_words = []

        result = []
        list_unique_words = set(list_words)

        sentence_generator = SentenceGeneratorModel()

        def choice_word_to_gen_sentence():
            number_choice_word = random.randint(1, 4)

            available_words = list(list_unique_words)
            if number_choice_word <= len(available_words):
                choice_word = random.sample(available_words, number_choice_word)
                for w in choice_word:
                    list_unique_words.remove(w)
            else:
                # Lấy tất cả từ còn lại và thêm từ nltk_words
                choice_word = available_words.copy()
                remaining = number_choice_word - len(choice_word)
                additional_words = random.sample(nltk_words, remaining)
                choice_word += additional_words
                list_unique_words.clear()

            return choice_word

        for _ in range(num_question):
            list_choice_word = choice_word_to_gen_sentence()

            # 1. Generate a simple sentence using a template
            sentence = sentence_generator.generate_sentence_from_words(list_choice_word, )
            # 2. Randomly choose a word to make incorrect in sequence
            sentence_words = sentence.strip(".").split()
            correct_word = random.sample(list(set(sentence_words)), 1)[0]
            sentence_words.remove(correct_word)

            # 3. Replace it with a grammatically incorrect word
            incorrect_word = self.create_incorrect_word(correct_word)
            modified_sentence = sentence.replace(correct_word, incorrect_word, 1)

            # 4. Create choices (including incorrect_word and distractors)
            choices = random.sample(list(set(sentence_words)), num_ans_per_question -1) + incorrect_word

            random.shuffle(choices)
            result.append({
                "question": modified_sentence,
                "type": QuestionTypeEnum.INCORRECT_WORD,
                "choices": choices,
                "answer": choices.index(incorrect_word),
                "explain": ["Correct: {sequence}"],
            })

        return result

    @staticmethod
    def create_incorrect_word(word: str) -> Optional[str]:
        list_transform_type = list(TransformWordType)
        random.shuffle(list_transform_type)
        for t in list_transform_type:
            transformer = transform_word_instance(t)
            incorrect_word = transformer.transform_word(word)
            if incorrect_word is not None and incorrect_word != word:
                return incorrect_word

        try:
            return random.choice(nltk_words) if nltk_words else None
        except ImportError:
            return None