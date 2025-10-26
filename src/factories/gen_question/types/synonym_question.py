from typing import List
import random

from src.factories.gen_question.types.base import Question, nltk_words
from src.enums import QuestionTypeEnum


class SynonymsQuestion(Question):
    """
    This class generates multiple-choice questions that ask the user
    to select a synonym for a given word.

    It uses dictionary data (from fetch_word_data) to retrieve
    meanings and synonyms. If the input list is empty or invalid,
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
            Randomly selects a word and finds one of its synonyms.

            Returns:
                tuple(str, str): question_word, synonym_answer
            """
            # Try from provided list word
            while list_unique_words:
                source_word = random.sample(list(list_unique_words), 1)[0]
                list_unique_words.remove(source_word)
                synonym_word = self.get_synonym(source_word)
                if synonym_word in list_unique_words:
                    list_unique_words.remove(source_word)
                if synonym_word:
                    return source_word, synonym_word

            # Fallback: use nltk_words
            while True:
                source_word = random.choice(nltk_words)
                synonym_word = self.get_synonym(source_word)
                if synonym_word:
                    return source_word, synonym_word

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
                "type": QuestionTypeEnum.SYNONYM,
                "choices": choices,
                "answer": choices.index(correct_answer),
                "explain": [],
            })

        return result

    def get_synonym(self, word: str):
        """
        Retrieves a random synonym for the given word using dictionary API data.

        It checks both the 'meanings.synonyms' and 'meanings.definitions.synonyms' fields.

        Args:
            word (str): The input word to find a synonym for.

        Returns:
            str or None: A synonym if found, else None.
        """
        data = self.fetch_word_data(word)
        if not data:
            return None

        meanings = data.get("meanings", [])

        # Randomly search for synonyms in the meaning entries
        while meanings:
            meaning = random.sample(meanings, 1)[0]

            # Try top-level synonyms
            synonyms = meaning.get("synonyms", [])

            # Also check synonyms inside definitions
            if not synonyms:
                definitions = meaning.get("definitions", [])
                for definition in definitions:
                    synonyms.extend(definition.get("synonyms", []))

            if synonyms:
                return random.choice(synonyms)

            meanings.remove(meaning)

        return None
