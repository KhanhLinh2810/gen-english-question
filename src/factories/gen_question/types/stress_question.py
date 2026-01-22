from typing import List
from collections import defaultdict
import random

from src.factories.gen_question.types.base import Question
from src.enums import QuestionTypeEnum, QuestionContentEnum
from src.utils.number import rand_exclude
from src.loaders.elastic import Elastic


class StressQuestion(Question):
    INDEX = 'phonetic_ipa_segement'

    def generate_questions(self, list_words: List[str] = None, num_question: int = 1, num_ans_per_question: int = 4, cefr: int = 3):
        if list_words is None:
            list_words = []

        result = []

        # Process data: group words by stress pattern
        num_word_in_list_per_question = self.cal_num_word_in_list_available_per_question(len(list_words), num_question, num_ans_per_question)
        stress_groups = self.stress_groups_from_list_words(list_words, cefr=cefr)

        # create
        def choice_random_words_in_stress_group(stress_group_key: int):
            stress_group = stress_groups[stress_group_key]
            item = random.choice(stress_group)
            stress_group.remove(item)  # Remove to avoid reuse within the same question
            return item["word"], item["ipa"]

        for _ in range(num_question):
            choices = []
            list_stress_group_keys = list(stress_groups.keys())

            # Get word with different stress
            if list_stress_group_keys:
                different_stress = random.choice(list_stress_group_keys)
                list_stress_group_keys.remove(different_stress)
                different_word_ipa = choice_random_words_in_stress_group(different_stress)
                different_word, different_ipa = different_word_ipa
            else:
                different_stress = random.randint(1, 4)
                list_different_word_ipa = self.get_random_word_and_ipa_by_stress_is_only_one_stress(different_stress)
                if different_word_ipa is None:
                    continue  # Skip this question if no valid word is found
                different_word, different_ipa = list_different_word_ipa[0]

            choices.append({
                "content": different_word,
                "explaination": different_ipa
            })

            # Get words with common stress
            if list_stress_group_keys:
                common_stress = random.choice(list_stress_group_keys)
                while len(choices) < num_word_in_list_per_question and stress_groups[common_stress]:
                    common_word_ipa = choice_random_words_in_stress_group(common_stress)
                    common_word, common_ipa = common_word_ipa
                    choices.append({
                        "content": common_word,
                        "explaination": common_ipa
                    })
            else:
                common_stress = rand_exclude(1, 4, different_stress)

            # Fill remaining choices from nltk_words if needed
            if len(choices) < num_ans_per_question:
                list_common_word_ipa = self.get_random_word_and_ipa_by_stress_is_only_one_stress(common_stress, num_ans_per_question-len(choices))
                if list_common_word_ipa:
                    for common_word_ipa in list_common_word_ipa:
                        common_word, common_ipa = common_word_ipa
                        choices.append({
                            "content": common_word,
                            "explaination": common_ipa
                        })


            final_choices = [({
                "content": c["content"],
                "explaination": c["explaination"],
                "is_correct": c["content"] == different_word
            }) for c in choices]
            result.append({
                "content": QuestionContentEnum.STRESS.value,
                "type": QuestionTypeEnum.STRESS,
                "choices": random.shuffle(final_choices)
            })
        return result

    def stress_groups_from_list_words(self, list_words: List[str]):
        es = Elastic()
        stress_groups = defaultdict(list)

        if not list_words:
            return stress_groups

        query = {
            "bool": {
                "must": [
                    {"terms": {"word": list_words}},
                    {"exists": {"field": "ipa"}},
                    {"exists": {"field": "stress"}},
                    {
                        "range": {
                            "num_syllables": {"gt": 1}
                        }
                    }
                ]
            }
        }

        resp = es.search(
            index=self.INDEX,
            query=query,
            size=len(list_words) * 4
        )

        hits = resp["hits"]["hits"]

        for hit in hits:
            doc = hit["_source"]
            word = doc["word"]
            stress = doc["stress"]
            ipa = doc.get("ipa")

            stress_groups[stress].append({
                "word": word,
                "ipa": ipa
            })

        return stress_groups
    
    def get_random_word_and_ipa_by_stress_is_only_one_stress(self, stress: int, num_word: int = 1):
        es = Elastic()

        must = [
            {"term": {"stress": stress}},
            {"term": {"is_only_one_stress": True}},
            {"exists": {"field": "ipa"}},
            {"exists": {"field": "word"}}
        ]
        # if cefr is not None:
        #     must.append({
        #         "range": {
        #             "cefr": {"gte": cefr - 1, "lte": cefr + 1}
        #         }
        #     })
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
            size=num_word*3,
            from_=offset
        )
        hits = resp["hits"]["hits"]

        results = []
            
        for hit in hits:
                doc = hit["_source"]
                word = doc.get("word")
                ipa = doc.get("ipa")
                
                if word and ipa:
                    results.append((word, ipa))
            
        if not results:
                return None
        
        random.shuffle(results)
        return results[:num_word]  

