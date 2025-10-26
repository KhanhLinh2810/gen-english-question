from typing import List, Optional
import random

from enums.question import QuestionTypeEnum
from src.enums.word import TransformWordType
from src.factories.gen_question.types.base import Question, nltk_words
from src.factories.transform_word.factory import transform_word_instance
from src.services.AI.sentence_generator import SentenceGeneratorModel


class FillInBlankQuestion(Question):
    """
    This class generates multiple-choice 'fill in the blank' questions.

    It picks a word, generates a sentence containing it, replaces it with a blank,
    and provides several answer choices (one correct and others incorrect).
    """

    def generate_questions(self, list_words: List[str], num_question: int = 1, num_ans_per_question: int = 4):
        if not list_words:
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

            # 1. Generate a sentence using chosen words
            sentence = sentence_generator.generate_sentence_from_words(list_choice_word)

            # 2. Randomly select one target word to blank out
            sentence_words = sentence.strip(".").split()
            target_word = random.choice(sentence_words)

            # 3. Replace the word with a blank
            modified_sentence = sentence.replace(target_word, "_____", 1)

            # 4. Generate incorrect (distractor) options
            incorrect_choices = self.create_incorrect_options(target_word, num_ans_per_question - 1)
            all_choices = incorrect_choices + [target_word]
            random.shuffle(all_choices)

            result.append({
                "question": modified_sentence,
                "type": QuestionTypeEnum.FILL_IN_BLANK,
                "choices": all_choices,
                "answer": all_choices.index(target_word),
                "explain": [f"The correct word is '{target_word}'."],
            })

        return result

    @staticmethod
    def create_incorrect_options(word: str, num_distractors: int) -> List[str]:
        """Generate a list of incorrect forms of the given word."""
        list_transform_type = list(TransformWordType)
        random.shuffle(list_transform_type)
        distractors = set()

        for t in list_transform_type:
            transformer = transform_word_instance(t)
            transformed = transformer.transform_word(word)
            if transformed and transformed != word:
                distractors.add(transformed)
            if len(distractors) >= num_distractors:
                break

        if len(distractors) < num_distractors and nltk_words:
            additional = random.sample(nltk_words, num_distractors - len(distractors))
            distractors.update(additional)

        return list(distractors)
