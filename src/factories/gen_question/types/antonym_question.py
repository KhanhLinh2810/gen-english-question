from typing import List
import random

from src.factories.gen_question.types.base import Question, nltk_words
from src.enums import QuestionTypeEnum


class AntonymsQuestion(Question):
    """
    This class generates multiple-choice questions that ask the user
    to select an antonym for a given word.

    It uses dictionary data (from fetch_word_data) to retrieve
    meanings and antonyms. If the input list is empty or invalid,
    it falls back to randomly chosen words from a built-in word list (nltk_words).
    """

    def generate_questions(self, list_words: List[str] = None, num_question: int = 1, num_ans_per_question: int = 4):
        if list_words is None:
            list_words = []

        result = []
        list_unique_words = set(list_words)

        # Internal helper function to get a valid question/answer pair
        def get_question_and_answer():
            """
            Randomly selects a word and finds one of its antonyms.

            Returns:
                tuple(str, str): question_word, antonym_answer
            """
            # Try from provided list word
            while list_unique_words:
                source_word = random.sample(list(list_unique_words), 1)[0]
                list_unique_words.remove(source_word)
                antonym_word = self.get_antonym(source_word)
                if antonym_word in list_unique_words:
                    list_unique_words.remove(antonym_word)
                if antonym_word:
                    return source_word, antonym_word

            # Fallback: use nltk_words
            while True:
                source_word = random.choice(nltk_words)
                antonym_word = self.get_antonym(source_word)
                if antonym_word:
                    return source_word, antonym_word

        for _ in range(num_question):
            question_word, correct_answer = get_question_and_answer()

            choices = [correct_answer]
            distractor_set = set()

            while len(choices) < num_ans_per_question:
                distractor_word = random.choice(nltk_words)

                if (distractor_word.lower() != correct_answer.lower() and
                    distractor_word.lower() != question_word.lower() and
                    distractor_word.lower() not in distractor_set):
                    distractor_set.add(distractor_word)
                    choices.append(distractor_word)

            random.shuffle(choices)

            result.append({
                "question": question_word,
                "type": QuestionTypeEnum.ANTONYM,
                "choices": choices,
                "answer": choices.index(correct_answer),
                "explain": [],
            })

        return result

    def get_antonym(self, word: str):
        """
        Retrieves a random antonym for the given word using dictionary API data.

        It checks both the 'meanings.antonyms' and 'meanings.definitions.antonyms' fields.

        Args:
            word (str): The input word to find an antonym for.

        Returns:
            str or None: An antonym if found, else None.
        """
        data = self.fetch_word_data(word)
        if not data:
            return None

        meanings = data.get("meanings", [])

        # Randomly search for antonyms in the meaning entries
        while meanings:
            meaning = random.sample(meanings, 1)[0]

            # Try top-level antonyms
            antonyms = meaning.get("antonyms", [])

            # Also check antonyms inside definitions
            if not antonyms:
                definitions = meaning.get("definitions", [])
                for definition in definitions:
                    antonyms.extend(definition.get("antonyms", []))

            if antonyms:
                return random.choice(antonyms)

            meanings.remove(meaning)

        return None
