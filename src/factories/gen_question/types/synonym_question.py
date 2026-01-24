from typing import List
import random

from src.factories.gen_question.types.base import Question
from src.enums import QuestionTypeEnum, QuestionContentEnum
from src.loaders.elastic import Elastic

from src.services.AI.false_ans_generator import FalseAnswerGenerator


class SynonymsQuestion(Question):
    INDEX = "meaning_vocabulary"
    false_ans_gen: FalseAnswerGenerator = None


    def generate_questions(self, list_words: List[str] = None, num_question: int = 1,
                           num_ans_per_question: int = 4, cefr: int = 3):

        list_words = list_words or []
        list_unique_words = set(list_words)
        random.shuffle(list_unique_words)

        result = []
        used_words = set()
        false_ans_gen = FalseAnswerGenerator()

        for _ in range(num_question):
            question_word, correct_answer, list_synonym_with_question_word = \
                self._pick_question_word(list_unique_words, used_words, cefr)

            choices = [{
                "content": correct_answer,
                "is_correct": True
            }]

            distractors = false_ans_gen.generate_distractors_from_antonyms_and_synonyms(
                correct_words=[correct_answer, question_word],
                num_distractors=num_ans_per_question - 1,
                list_exclude_word  = list_synonym_with_question_word
            )
            for d in distractors:
                choices.append({
                    "content": d.lower(),
                    "is_correct": False
                })
            random.shuffle(choices)

            result.append({
                "content": QuestionContentEnum.SYNONYM.value.format(word=question_word),
                "type": QuestionTypeEnum.SYNONYM,
                "choices": choices,
            })

        return result
    
    # -----------------------------------------------------
    # Lấy tất cả synonym của 1 từ từ ES (nhiều nghĩa)
    # -----------------------------------------------------
    def get_list_synonym(self, word: str):
        es = Elastic()
        query = {"term": {"word.keyword": word.lower()}}
        resp = es.search(index=self.INDEX, query=query, size=1000)

        hits = resp["hits"]["hits"]
        if not hits:
            return []

        synonyms = set()
        for h in hits:
            s = h["_source"].get("synonyms", [])
            synonyms.update(s)

        return list(synonyms)
    
    # -----------------------------------------------------
    # Lấy 1 từ làm câu hỏi và 1 synonym làm đáp án
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

            syns = self.get_list_synonym(source)
            valid_syns = [s for s in syns if s not in used_words]
            if not valid_syns:
                continue

            correct = random.choice(valid_syns)
            return source, correct, valid_syns
        # return source, correct, set(syns)

        # FALLBACK ES
        while True:
            doc = self.get_random(self.INDEX, None, cefr=cefr)
            if not doc:
                continue

            source = doc["word"]

            if source in used_words:
                continue

            syns = self.get_list_synonym(source)
            valid_syns = [s for s in syns if s not in used_words]
            if not valid_syns:
                continue

            return source, random.choice(valid_syns), valid_syns
            # return source, random.choice(valid_syns), set(syns)
