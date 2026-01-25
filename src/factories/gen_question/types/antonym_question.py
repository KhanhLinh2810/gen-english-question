from typing import List
import random

from src.factories.gen_question.types.base import Question
from src.enums import QuestionTypeEnum, QuestionContentEnum

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

        for _ in range(num_question):
            question_word, correct_answer = \
                self._pick_question_word(list_unique_words, used_words, cefr)

            choices = [correct_answer]

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
                "content": QuestionContentEnum.ANTONYM.value.format(word=question_word),
                "type": QuestionTypeEnum.ANTONYM,
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
