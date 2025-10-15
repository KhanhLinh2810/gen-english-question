import random
from collections import defaultdict
from typing import List
from src.factories.gen_question.base import Question, nltk_words
from src.enum.question import QuestionTypeEnum

from src.utils.number import rand_exclude
from src.utils.word import get_stress_pattern, convert_word_to_ipa


class StressQuestion(Question):
    def generate_questions(self, list_words: List[str], num_question: int = 1, num_ans_per_question: int = 4):
        result = []

        # process data:
        stress_groups = defaultdict(list)
        for word in list_words:
            stress = get_stress_pattern(word)
            ipa = convert_word_to_ipa(word)
            if ipa is None or stress is None:
                continue
            stress_groups[stress].append({"word": word, "ipa": ipa})
        num_word_in_list_per_question = self.cal_num_word_in_list_available_per_question(len(list_words), num_question, num_ans_per_question)

        # create
        def choice_random_words_in_stress_group(stress_group_key):
            stress_group = stress_groups[stress_group_key]
            item = random.choice(stress_group)
            stress_group.remove(item)
            return item["word"], item["ipa"]

        for _ in range(num_question): # type: ignore
            choices = []
            explain = []
            list_stress_group_keys = list(stress_groups.keys())

            # get different stress
            if len(list_stress_group_keys) != 0:
                different_stress = random.choice(list_stress_group_keys)
                list_stress_group_keys.remove(different_stress)
                different_word, different_ipa = choice_random_words_in_stress_group(different_stress)
            else:
                different_stress = random.randint(1, 3)
                different_word, different_ipa = self.get_random_word_and_ipa_by_stress(different_stress)

            choices.append(different_word)
            explain.append(f'{different_word} ({different_ipa})')

            # get common stress
            if len(list_stress_group_keys) != 0:
                # if in list word exist more two stresses, get choice in list word
                common_stress = random.choice(list_stress_group_keys)
                list_stress_group_keys.remove(common_stress)
                # number of choice must be lesster number of list word slipt number of question and in stress group must exist item
                while len(choices) < num_word_in_list_per_question and len(stress_groups[common_stress]) > 0:
                    common_word, common_ipa = choice_random_words_in_stress_group(common_stress)

                    choices.append(common_word)
                    explain.append(f'{common_word} ({common_ipa})')
            else:
                common_stress = rand_exclude(1, 3, different_stress)

            # maybe after get choice in list word, number of choice is not enough, so get choice in local data
            while len(choices) < num_ans_per_question:
                common_word, common_word_ipa = self.get_random_word_and_ipa_by_stress(common_stress)

                choices.append(common_word)
                explain.append(f'{common_word} ({common_word_ipa})')
                continue

            random.shuffle(choices)

            result.append({
                "question": "",
                "type": QuestionTypeEnum.STRESS,
                "choices": choices,
                "answer": choices.index(different_word),
                "explain": explain,
            })

        return result

    def get_random_word_and_ipa_by_stress(self, stress: int):
        while True:
            word = random.choice(nltk_words)
            word_ipa = convert_word_to_ipa(word)
            word_stress = get_stress_pattern(word)
            if word_ipa is None or word_stress is None:
                nltk_words.remove(word)
                continue
            if word_stress == stress:
                return word, word_ipa


