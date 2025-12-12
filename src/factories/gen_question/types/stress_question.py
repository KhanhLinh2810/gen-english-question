from typing import List
from collections import defaultdict
import random

from src.factories.gen_question.types.base import Question
from src.enums import QuestionTypeEnum
from src.utils.number import rand_exclude
from src.utils.word import get_stress_pattern, convert_word_to_ipa
from src.loaders.elastic import Elastic


class StressQuestion(Question):
    INDEX = 'phonetic'

    def generate_questions(self, list_words: List[str] = None, num_question: int = 1, num_ans_per_question: int = 4, cefr: int = 3):
        if list_words is None:
            list_words = []

        result = []

        # Process data: group words by stress pattern
        num_word_in_list_per_question = self.cal_num_word_in_list_available_per_question(len(list_words), num_question, num_ans_per_question)

        stress_groups = defaultdict(list)
        for word in list_words:
            list_doc = self.get_list_word(index=self.INDEX,
                query = {
                "bool": {
                    "must": {
                        "term": {"word.keyword": word}
                    }
            }})


            for doc in list_doc:
                if "stress" not in doc or "ipa" not in doc:
                    continue
                stress_groups[doc["stress"]].append({
                    "word": word, 
                    "ipa": doc["ipa"]
                })

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
                    "content": "",
                    "type": QuestionTypeEnum.STRESS,
                    "choices": choices,
                    "answer": choices.index(different_word),
                    "explain": explain,
                })

        return result

    def get_random_word_and_ipa_by_stress(self, stress: int, cefr: int = None):
        es = Elastic()

        must = [
            {"term": {"stress": stress}},
            {"exists": {"field": "ipa"}},
            {"exists": {"field": "word"}}
        ]
        if cefr is not None:
            must.append({
                "range": {
                    "cefr": {"gte": cefr - 1, "lte": cefr + 1}
                }
            })
        query = {
            "bool": {"must": must}
        }

        total_doc = es.count(index=self.INDEX, query=query)["count"]
        if total_doc == 0:
            return None

        offset = random.randint(0, total_doc - 1)
        resp = es.search(
            index=self.INDEX,
            query=query,
            size=1,
            from_=offset
        )
        hits = resp["hits"]["hits"]

        if hits:        
            doc = hits[0]["_source"] 
            if "word" in doc and "ipa" in doc:
                return doc["word"], doc["ipa"]
            
        return None

