from typing import List
import random

from src.factories.gen_question.types.base import Question, nltk_words
from src.enums import QuestionTypeEnum

from src.loaders.elastic import Elastic
from src.services.AI.false_ans_generator import FalseAnswerGenerator



class AntonymsQuestion(Question):
    INDEX = "vocabulary"
    false_ans_gen: FalseAnswerGenerator = None

    def __init__(self):
        if self.false_ans_gen is None:
            self.false_ans_gen = FalseAnswerGenerator()

    def generate_questions(self, list_words: List[str] = None, num_question: int = 1,
                           num_ans_per_question: int = 4, cefr: int = 3):

        list_words = list_words or []
        list_unique_words = set(list_words)

        result = []
        used_words = set()
        used_choices = set()

        for _ in range(num_question):
            question_word, correct_answer = \
                self._pick_question_word(list_unique_words, used_words, cefr)
            
            # max_loop = 100
            # pos = self.get_pos({
            #     "bool": {
            #         "must": [
            #             {"term": {"word.keyword": question_word.lower()}},
            #             {"term": {"antonyms.keyword": correct_answer.lower()}}
            #         ]
            #     }
            # })
            # used_words.update([question_word, correct_answer])

            choices = [correct_answer]

            # while len(choices) < num_ans_per_question and max_loop > 0:
            #     doc = self.get_random(self.INDEX, None, cefr=cefr, pos=pos)
            #     if not doc:
            #         continue

            #     candidate = doc["word"]

            #     # Loại trừ điều kiện chung
            #     if (
            #         candidate in used_choices or
            #         candidate in used_words or
            #         candidate in antonym_set or
            #         candidate == question_word or
            #         candidate == correct_answer
            #     ):
            #         continue

            #     # Loại distractor có nghĩa trùng với đáp án
            #     syns = set(self.get_list_antonym(candidate))
            #     if correct_answer in syns:
            #         continue

            #     choices.append(candidate)
            #     used_choices.add(candidate)
            #     max_loop -= 1



            distractors = self.false_ans_gen.generate_distractors_from_antonyms(
                target_word=[correct_answer, question_word],
                num_false_answers=num_ans_per_question - 1
            )
            choices.extend(distractors)
            random.shuffle(choices)

            final_choices = []
            for c in choices:
                final_choices.append({
                    "content": c,
                    "is_correct": c == correct_answer
                })

            result.append({
                "content": question_word,
                "type": QuestionTypeEnum.SYNONYM,
                "choices": final_choices,
            })

        return result
    
    # -----------------------------------------------------
    # Lấy tất cả antonym của 1 từ từ ES (nhiều nghĩa)
    # -----------------------------------------------------
    def get_list_antonym(self, word: str):
        es = Elastic()
        query = {"term": {"word.keyword": word.lower()}}
        resp = es.search(index=self.INDEX, query=query, size=1000)

        hits = resp["hits"]["hits"]
        if not hits:
            return []

        antonyms = set()
        for h in hits:
            s = h["_source"].get("antonyms", [])
            antonyms.update(s)

        return list(antonyms)
    
    # -----------------------------------------------------
    # Lấy 1 từ làm câu hỏi và 1 antonym làm đáp án
    # -----------------------------------------------------
    def _pick_question_word(self, list_unique_words, used_words, cefr):
        """
        - Ưu tiên lấy từ danh sách đầu vào
        - Nếu hết → lấy từ ES random theo CEFR
        """

        # ƯU TIÊN INPUT LIST
        while list_unique_words:
            source = list_unique_words.pop()

            if source in used_words:
                continue

            syns = self.get_list_antonym(source)
            valid_syns = [s for s in syns if s not in used_words]
            if not valid_syns:
                continue

            correct = random.choice(valid_syns)
            return source, correct

        # FALLBACK ES
        while True:
            doc = self.get_random(self.INDEX, None, cefr=cefr)
            if not doc:
                continue

            source = doc["word"]

            if source in used_words:
                continue

            syns = self.get_list_antonym(source)
            valid_syns = [s for s in syns if s not in used_words]
            if not valid_syns:
                continue

            return source, random.choice(valid_syns)
