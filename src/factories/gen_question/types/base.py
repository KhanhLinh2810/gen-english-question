from abc import ABC, abstractmethod
from typing import Set, Optional

import random

from src.loaders.elastic import Elastic
from src.llms.models import GeminiLLM, OpenAILLM



class Question(ABC):     
    def __init__(self, model='gemini'):
        if model == 'gemini':
            self.llm = GeminiLLM()
        else:
            self.llm = OpenAILLM()

    @abstractmethod
    def generate_questions(self, list_words: Set[str], num_questions: int = 1, num_ans_per_question: int = 4):
        pass

    def _build_query(self, query: dict = None, cefr: Optional[int] = None, pos: str = None):
        must = []
        if query:
            must.append(query)
        if cefr is not None:
            must.append({
                "range": {
                    "cefr": {"gte": cefr - 1, "lte": cefr + 1}
                }
            })
        if pos is not None:
            must.append({
                "term": {"pos.keyword": pos}
            })
        return {"bool": {"must": must}} if must else {"match_all": {}}
    
    # ---------------------------------------
    # Get 1 random doc from ES using CEFR + filter
    # ---------------------------------------
    def get_random(self, index: str, query: dict = None, cefr: int = None, pos: str = None):
        es = Elastic()
        q = self._build_query(query, cefr, pos)

        count = es.count(index=index, query=q)["count"]
        if count == 0:
            return None

        offset = random.randint(0, count - 1)

        resp = es.search(index=index, query=q, size=1, from_=offset)
        hits = resp["hits"]["hits"]
        return hits[0]["_source"] if hits else None

    # ---------------------------------------
    # Get first matched doc
    # ---------------------------------------
    def get_detail_word(self, index: str, query: dict = None):
        es = Elastic()
        q = self._build_query(query)
        resp = es.search(index=index, query=q, size=1)
        hits = resp["hits"]["hits"]
        return hits[0]["_source"] if hits else None

    def get_cefr_word(self, index: str, word: str):
        doc = self.get_detail_word(index, {"term": {"word.keyword": word}})
        return doc.get("cefr") if doc else None

    # ---------------------------------------
    def check_valid_cefr(self, target_cefr: int, candidate_cefr: Optional[int]):
        if candidate_cefr is None:
            return False
        return abs(target_cefr - candidate_cefr) <= 1
    
    # ---------------------------------------
    # Get pos of word
    # ---------------------------------------
    def get_pos(self, index: str, query: dict = None):
        list_docs = self.get_list_word(index, query)

        if len(list_docs) > 0:
            doc = random.choice(list_docs)
            if doc and "pos" in doc:
                return doc["pos"]

        return "noun"
    
    def get_list_word(self, index: str, query: dict = None):
        es = Elastic()

        resp = es.search(
            index=index,
            query=query,
            size=1000   
        )
        hits = resp["hits"]["hits"]

        return [hit["_source"] for hit in hits] if hits else []
    
    # ---------------------------------------
    # process raw data of tool call
    # ---------------------------------------
    def _parse_raw_tool_output(self, raw_output, name_function, type):
        """
        Parse tool_calls output from LLM and return validated questions.
        """
        results = []
        # print(raw_output)

        if "tool_calls" not in raw_output or not raw_output["tool_calls"]:
            return results
        

        for call in raw_output["tool_calls"]:
            print(name_function, call)

            if call.get("name") != name_function:
                continue

            list_questions = call.get("arguments", {}).get("questions", [])
            print(list_questions)
            for q in list_questions:
                raw_choices = q.get("choices", [])
                list_answer = q.get("answer")

                if not raw_choices or not list_answer:
                    continue

                choices = []
                count_correct = 0

                for c in raw_choices:
                    is_correct = c in list_answer
                    choices.append({
                        "content": c,
                        "is_correct": is_correct
                    })
                    if is_correct:
                        count_correct += 1

                # reject invalid cases
                if count_correct == 0 or count_correct == len(choices):
                    continue

                results.append({
                    "content": q.get("content"),
                    "type": type,
                    "choices": choices,
                    "explanation": q.get("explanation"),
                    "tags": q.get("tags", []),
                })

        return results




    @staticmethod
    def cal_num_word_in_list_available_per_question(
            len_list_words: int,
            num_questions: int = 1,
            num_ans_per_question: int = 4
    ) -> int:
        return min(len_list_words//num_questions, num_ans_per_question)
      