from typing import List
from collections import defaultdict
import random

from src.factories.gen_question.base import Question, nltk_words
from src.enum.question import QuestionTypeEnum
from src.utils.number import rand_exclude
from src.utils.word import get_stress_pattern, convert_word_to_ipa


class StressQuestion(Question):
    def generate_questions(self, list_words: List[str] = None, num_question: int = 1, num_ans_per_question: int = 4):
        if list_words is None:
            list_words = []

        result = []

        # Process data: group words by stress pattern
        num_word_in_list_per_question = self.cal_num_word_in_list_available_per_question(len(list_words), num_question, num_ans_per_question)

        stress_groups = defaultdict(list)
        for word in list_words:
            stress = get_stress_pattern(word)
            ipa = convert_word_to_ipa(word)
            if ipa is None or stress is None:
                continue
            stress_groups[stress].append({"word": word, "ipa": ipa})

        # create
        def choice_random_words_in_stress_group(stress_group_key: int):
            stress_group = stress_groups[stress_group_key]
            item = random.choice(stress_group)
            stress_group.remove(item)  # Remove to avoid reuse within the same question
            return item["word"], item["ipa"]

        for _ in range(num_question):
            choices = []
            explain = []
            list_stress_group_keys = list(stress_groups.keys())

            # Get word with different stress
            if list_stress_group_keys:
                different_stress = random.choice(list_stress_group_keys)
                list_stress_group_keys.remove(different_stress)
                different_word_ipa = choice_random_words_in_stress_group(different_stress)
                different_word, different_ipa = different_word_ipa
            else:
                different_stress = random.randint(1, 3)
                different_word_ipa = self.get_random_word_and_ipa_by_stress(different_stress)
                if different_word_ipa is None:
                    continue  # Skip this question if no valid word is found
                different_word, different_ipa = different_word_ipa

            choices.append(different_word)
            explain.append(f'{different_word} ({different_ipa}, stress pattern: {different_stress})')

            # Get words with common stress
            if list_stress_group_keys:
                common_stress = random.choice(list_stress_group_keys)
                while len(choices) < num_word_in_list_per_question and stress_groups[common_stress]:
                    common_word_ipa = choice_random_words_in_stress_group(common_stress)
                    common_word, common_ipa = common_word_ipa
                    choices.append(common_word)
                    explain.append(f'{common_word} ({common_ipa}, stress pattern: {common_stress})')
            else:
                common_stress = rand_exclude(1, 3, different_stress)

            # Fill remaining choices from nltk_words if needed
            while len(choices) < num_ans_per_question:
                common_word_ipa = self.get_random_word_and_ipa_by_stress(common_stress)
                if common_word_ipa is None:
                    break  # Skip adding if no valid word is found
                common_word, common_ipa = common_word_ipa
                choices.append(common_word)
                explain.append(f'{common_word} ({common_ipa}, stress pattern: {common_stress})')

            # Only add the question if we have enough choices
            print(choices, len(choices))
            if len(choices) == num_ans_per_question:
                random.shuffle(choices)
                result.append({
                    "question": "",
                    "type": QuestionTypeEnum.STRESS,
                    "choices": choices,
                    "answer": choices.index(different_word),
                    "explain": explain,
                })

        print(result)

        return result

    @staticmethod
    def get_random_word_and_ipa_by_stress(stress: int):
        max_attempts = 10000
        attempts = 0
        while attempts < max_attempts:
            if not nltk_words:
                return None
            word = random.choice(nltk_words)
            word_ipa = convert_word_to_ipa(word)
            word_stress = get_stress_pattern(word)
            if word_ipa is None or word_stress is None:
                attempts += 1
                continue
            if word_stress == stress:
                return word, word_ipa
            attempts += 1
        return None  # Return None if no word is found