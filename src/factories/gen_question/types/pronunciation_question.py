import random
from typing import List, Dict, Optional, Set, Tuple
from collections import defaultdict

from src.loaders.elastic import Elastic
from src.enums.question import CHAR_TO_PHONEME, GRAPHEME_RULES, PHONEME_TO_CHAR, SUFFIX_RULES, VOWELS, QuestionContentEnum, QuestionTypeEnum
from src.factories.gen_question.types.base import Question


class PronunciationQuestion(Question):
    INDEX = "phonetic_ipa_segement"

    def generate_questions(
        self,
        list_words: List[str],
        num_question: int = 1,
        num_ans_per_question: int = 4
    ) -> List[dict]:
        result = []
        unique_words = list(set(list_words))

        word_data, groups = self._classify_words(unique_words, num_question)
        attempt = 0

        while len(result) < num_question and attempt < 20:
            question = self._try_generate_one_question(
                word_data, groups, num_ans_per_question
            )
            if question:
                result.append(question)
            else:
                attempt += 1

        return result

    def _try_generate_one_question(
        self,
        word_data: Dict[str, List[dict]],
        groups: Dict[str, List[dict]],
        num_choices: int
    ) -> Optional[dict]:        
        suffix_key = self._pick_non_empty_group(groups, SUFFIX_RULES.keys())
        grapheme_key = self._pick_non_empty_group(groups, GRAPHEME_RULES.keys())

        available_cases = []
        if word_data:
            available_cases.append(1)
        if suffix_key:
            available_cases.append(2)
        if grapheme_key:
            available_cases.append(3)
        if available_cases:
            switch_case = random.choice(available_cases)
        else:
            return None

        if switch_case == 1:
            return self._create_vowel_or_letter_question(word_data, num_choices)

        # Strategy 2: Suffix / special ending rules
        if switch_case == 2:
            return self._create_suffix_question(
                groups[suffix_key],
                suffix_key,
                SUFFIX_RULES[suffix_key],
                num_choices
            )

        # Strategy 3: Grapheme → phoneme mapping confusion
        if switch_case == 3:
            return self._create_grapheme_question(
                groups[grapheme_key],
                grapheme_key,
                GRAPHEME_RULES[grapheme_key],
                num_choices
            )

        return None

    # ────────────────────────────────────────────────
    #  Helper - pick a group that still has items
    # ────────────────────────────────────────────────
    def _pick_non_empty_group(self, groups: dict, allowed_keys) -> Optional[str]:
        candidates = [k for k in allowed_keys if k in groups and groups[k]]
        return random.choice(candidates) if candidates else None

    # ────────────────────────────────────────────────
    #  1. Vowel / letter pronunciation confusion
    # ────────────────────────────────────────────────
    def _create_vowel_or_letter_question(
        self,
        word_data: Dict[str, List[dict]],
        num_choices: int
    ) -> Optional[dict]:
        if not word_data:
            return None
        
        base_word = random.choice(list(word_data.keys()))
        variants = word_data.pop(base_word, [])
        if not variants:
            return None

        sample = random.choice(variants)
        seg_word = sample["segement_word"]
        seg_ipa = sample["segement_ipa"]

        # Find first vowel position that has clear mapping
        vowel_pos = None
        for i, (char, ipa) in enumerate(zip(seg_word, seg_ipa)):
            if ipa in VOWELS and char in PHONEME_TO_CHAR.get(ipa, set()):
                vowel_pos = i
                break

        if vowel_pos is None:
            return None

        answer_char = seg_word[vowel_pos]
        answer_ipa = seg_ipa[vowel_pos]

        # Collect all possible IPAs for this position & char
        all_ipas_at_pos = {
            v["segement_ipa"][vowel_pos]
            for v in variants
            if len(v["segement_ipa"]) > vowel_pos
        }

        possible_distractors = [
            ipa for ipa in CHAR_TO_PHONEME.get(answer_char, [])
            if ipa != answer_ipa and ipa not in all_ipas_at_pos
        ]

        if not possible_distractors:
            return None

        distractor_ipa = random.choice(possible_distractors)

        distractors = self._fetch_distractors_by_char_ipa(
            char=answer_char,
            ipa=distractor_ipa,
            exclude_words={base_word},
            limit=num_choices * 3
        )

        choices = self._build_choices(
            correct={
                "word": base_word,
                "ipa": sample["ipa"],
                "segments_word": seg_word,
                "segments_ipa": seg_ipa,
                "highlight_char": answer_char,
                "highlight_ipa": answer_ipa
            },
            distractors=distractors,
            highlight_char=answer_char,
            highlight_ipa=distractor_ipa,
            num_choices=num_choices
        )

        if not choices:
            return None

        random.shuffle(choices)

        return {
            "content": QuestionContentEnum.PRONUNCIATION,
            "type": QuestionTypeEnum.PRONUNCIATION,
            "choices": choices
        }

    # ────────────────────────────────────────────────
    #  2. Suffix pronunciation (s/es/ed)
    # ────────────────────────────────────────────────
    def _create_suffix_question(
        self,
        group: List[dict],
        suffix: str,
        possible_ipas: List[str],
        num_choices: int
    ) -> Optional[dict]:
        if not group:
            return None

        correct_item = random.choice(group)
        group.remove(correct_item)  # remove to avoid reuse in same batch

        last_ipa = correct_item["segement_ipa"][-1]

        distractor_ipa = self._choose_different_ipa(possible_ipas, last_ipa)
        if not distractor_ipa:
            return None

        distractors = self._fetch_distractors_by_suffix_ipa(
            suffix=suffix,
            ipa=distractor_ipa,
            exclude_words={correct_item["word"]},
            limit=num_choices * 3
        )

        choices = self._build_choices(
            correct={
                "word": correct_item["word"],
                "ipa": correct_item["ipa"],
                "segments_word": correct_item["segement_word"],
                "segments_ipa": correct_item["segement_ipa"],
            },
            distractors=distractors,
            num_choices=num_choices,
            suffix=suffix
        )

        if not choices:
            return None

        random.shuffle(choices)
        return {
            "content": QuestionContentEnum.PRONUNCIATION,
            "type": QuestionTypeEnum.PRONUNCIATION,
            "choices": choices
        }

    # ────────────────────────────────────────────────
    #  3. Grapheme → phoneme confusion (th, ch, t, d, ...)
    # ────────────────────────────────────────────────
    def _create_grapheme_question(
        self,
        group: List[dict],
        grapheme: str,
        possible_ipas: List[str],
        num_choices: int
    ) -> Optional[dict]:
        if not group:
            return None

        correct_item = random.choice(group)
        seg_word = correct_item["segement_word"]
        seg_ipa = correct_item["segement_ipa"]

        # Find first occurrence of grapheme
        pos = None
        answer_ipa = None
        for i, char in enumerate(seg_word):
            if char == grapheme:
                pos = i
                answer_ipa = seg_ipa[i]
                break

        if pos is None or answer_ipa is None:
            return None

        distractor_ipa = self._choose_different_ipa(possible_ipas, answer_ipa)
        if not distractor_ipa:
            return None

        es = Elastic()
        distractors = self._fetch_distractors_by_char_ipa(
            char=grapheme,
            ipa=distractor_ipa,
            exclude_words={correct_item["word"]},
            limit=num_choices * 3
        )

        choices = self._build_choices(
            correct={
                "word": correct_item["word"],
                "ipa": correct_item["ipa"],
                "segments_word": seg_word,
                "segments_ipa": seg_ipa,
                "highlight_char": grapheme,
                "highlight_ipa": answer_ipa,
            },
            distractors=distractors,
            highlight_char=grapheme,
            highlight_ipa=distractor_ipa,
            num_choices=num_choices
        )

        if not choices:
            return None

        random.shuffle(choices)
        return {
            "content": QuestionContentEnum.PRONUNCIATION,
            "type": QuestionTypeEnum.PRONUNCIATION,
            "choices": choices
        }

    # ────────────────────────────────────────────────
    #  Common choice builder
    # ────────────────────────────────────────────────
    def _build_choices(
        self,
        correct: dict,
        distractors: List[dict],
        num_choices: int,
        highlight_char: Optional[str] = None,
        highlight_ipa: Optional[str] = None,
        suffix: Optional[str] = None,
        **kwargs
    ) -> List[dict]:

        def default_format(segments_word, segments_ipa, c, ip):
            if suffix:
                if not segments_word:
                    return ""
                return "".join(segments_word[:-1]) + "_" + suffix + "_"
            parts = []
            for w, p in zip(segments_word, segments_ipa):
                if w == c and p == ip:
                    parts.append(f"_{w}_")
                else:
                    parts.append(w)
            return "".join(parts)
        
        choices = [{
            "content": default_format(
                correct["segments_word"],
                correct["segments_ipa"],
                correct.get("highlight_char", None),
                correct.get("highlight_ipa", None)
            ),
            "is_correct": True,
            "explanation": correct["ipa"]
        }]

        used = {correct["word"]}

        for doc in random.sample(distractors, k=len(distractors)):
            word = doc["word"]
            if word in used:
                continue

            content = default_format(
                doc["segement_word"],
                doc["segement_ipa"],
                highlight_char or "",
                highlight_ipa or ""
            )

            if "_" not in content:  # skip invalid formatting
                continue

            choices.append({
                "content": content,
                "is_correct": False,
                "explanation": doc["ipa"]
            })
            used.add(word)

            if len(choices) >= num_choices:
                break

        return choices[:num_choices]

    # ────────────────────────────────────────────────
    #  Elasticsearch helpers
    # ────────────────────────────────────────────────
    def _fetch_distractors_by_char_ipa(
        self,
        char: str,
        ipa: str,
        exclude_words: Set[str],
        limit: int = 30
    ) -> List[dict]:
        es = Elastic()
                                # if (doc['segments.char.keyword'].size() == 0) {
                                #     return false;
                                # }
                                
                                # for (int i = 0; i < doc['segments.char.keyword'].size(); i++) {
                                #     if (doc['segments.char.keyword'][i] == params.char && 
                                #         doc['segments.ipa.keyword'][i] == params.ipa) {
                                #         return true;
                                #     }
                                # }
                                # return false;

        query = {
            "bool": {
                "must": [{
                    "nested": {
                        "path": "segements",
                        "query": {
                            "bool": {
                                "must": [
                                    {"term": {"segements.char": char}},
                                    {"term": {"segements.ipa": ipa}}
                                ]
                            }
                        }
                    }
                }],
                "must_not": [{
                    "terms": {
                        "word": list(exclude_words)
                    }
                }]
            }
        }

        try:
            count = es.count(index=self.INDEX, query=query).get("count", 0)
            size = min(limit, max(1, count))
            from_ = random.randint(0, max(0, count - size))

            res = es.search(
                index=self.INDEX,
                query=query,
                size=size,
                from_=from_,
                explain=True
            )
            return [h["_source"] for h in res["hits"]["hits"]]
        except Exception as e:
            print(f"ES error (char-ipa): {e}")
            return []

    def _fetch_distractors_by_suffix_ipa(
        self,
        suffix: str,
        ipa: str,
        exclude_words: Set[str],
        limit: int = 30
    ) -> List[dict]:
        es = Elastic()

        query = {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "segements",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"term": {"segements.char": suffix}},
                                        {"term": {"segements.ipa": ipa}},
                                        {"term": {"segements.is_last_char": True}}
                                    ]
                                }
                            }
                        }
                    }
                ],
                "must_not": [{
                    "terms": {
                        "word": list(exclude_words)
                    }
                }]
            }
        }


        try:
            count = es.count(index=self.INDEX, query=query).get("count", 0)
            size = min(limit, max(1, count))
            from_ = random.randint(0, max(0, count - size))

            res = es.search(
                index=self.INDEX,
                query=query,
                size=size,
                from_=from_
            )
            return [h["_source"] for h in res["hits"]["hits"]]
        except Exception as e:
            print(f"ES error (suffix-ipa): {e}")
            return []

    def _choose_different_ipa(self, candidates: List[str], correct: str) -> Optional[str]:
        others = [p for p in candidates if p != correct]
        return random.choice(others) if others else None

    def _classify_words(self, words: List[str], num_question: int) -> Tuple[Dict[str, List[dict]], Dict[str, List[dict]]]:
        data = self.fetch_phonetic_data_batch(words, num_question)
        groups = defaultdict(list)

        all_keys = set(SUFFIX_RULES) | set(GRAPHEME_RULES)

        for word, variants in data.items():
            for variant in variants:
                item = {**variant, "word": word}
                sw = variant["segement_word"]
                si = variant["segement_ipa"]

                if len(sw) != len(si):
                    continue

                # suffix classification
                last_char = sw[-1] if sw else ""
                if last_char in SUFFIX_RULES:
                    groups[last_char].append(item)

                # grapheme classification
                for i, char in enumerate(sw):
                    if char in GRAPHEME_RULES:
                        groups[char].append(item)

        # Clean empty groups
        groups = {k: v for k, v in groups.items() if v}

        return data, groups

    def fetch_phonetic_data_batch(
        self,
        list_words: List[str],
        min_items_needed: int = 3,
    ) -> Dict[str, List[Dict]]:
        """
        Fetch phonetic segmentation data from Elasticsearch.

        Args:
            list_words: Danh sách từ cần ưu tiên lấy dữ liệu
            min_items_needed: Số lượng từ tối thiểu mong muốn có trong kết quả

        Returns:
            Dict[str, List[Dict]]: {word: [variant1, variant2, ...]}
            Mỗi variant chứa: {"ipa": str, "segement_ipa": list, "segement_word": list}
        """
        es = Elastic()
        data: Dict[str, List[Dict]] = defaultdict(list)
        seen_segments: Dict[str, Set[Tuple]] = defaultdict(set)

        # ───────────────────────────────────────
        # Phase 1: Lấy dữ liệu từ các từ được chỉ định
        # ───────────────────────────────────────
        if list_words:
            self._fetch_and_deduplicate(
                es=es,
                words=list_words,
                data=data,
                seen_segments=seen_segments,
                size=len(list_words) * 5
            )

        # ───────────────────────────────────────
        # Phase 2: Bổ sung thêm từ ngẫu nhiên nếu chưa đủ
        # ───────────────────────────────────────
        if min_items_needed < 10:
            buffer = 3
        elif min_items_needed < 50:
            buffer = 10
        else:
            buffer = 20

        target_count = min_items_needed + buffer
        if len(data) < target_count:
            self._fetch_random_additional(
                es=es,
                data=data,
                seen_segments=seen_segments,
                target_count=target_count,
                max_attempts=20,
                batch_size=min_items_needed*3
            )

        return dict(data)  

    def _fetch_and_deduplicate(
        self,
        es: Elastic,
        words: List[str],
        data: Dict[str, List[Dict]],
        seen_segments: Dict[str, Set[Tuple]],
        size: int
    ) -> None:
        """Lấy dữ liệu cho danh sách từ cụ thể và loại bỏ trùng lặp segmentation"""
        query = self._base_query(words)

        try:
            resp = es.search(index=self.INDEX, query=query, size=size)
            self._process_hits(resp, data, seen_segments)
        except Exception as e:
            print(f"[fetch_and_deduplicate] Elasticsearch error: {e}")

    def _fetch_random_additional(
        self,
        es: Elastic,
        data: Dict[str, List[Dict]],
        seen_segments: Dict[str, Set[Tuple]],
        target_count: int,
        max_attempts: int = 20,
        batch_size: int = 30
    ) -> None:
        """Bổ sung từ ngẫu nhiên cho đến khi đủ số lượng mong muốn"""
        total_docs = es.count(index=self.INDEX).get("count", 0)
        if total_docs <= len(data):
            return

        attempts = 0
        while len(data) < target_count and attempts < max_attempts:
            attempts += 1
            offset = random.randint(0, max(0, total_docs - batch_size))

            try:
                resp = es.search(
                    index=self.INDEX,
                    query=self._base_query(),  # không filter word → lấy random
                    size=batch_size,
                    from_=offset
                )
                self._process_hits(resp, data, seen_segments)
            except Exception as e:
                print(f"[fetch_random_additional] attempt {attempts} error: {e}")
                continue

    def _base_query(self, specific_words: List[str] = None) -> dict:
        """Query cơ bản, có thể lọc theo từ cụ thể"""
        must_clauses = [
            {"exists": {"field": "ipa"}},
            {"exists": {"field": "stress"}},
        ]
        if specific_words:
            must_clauses.append({"terms": {"word": specific_words}})

        return {"bool": {"must": must_clauses}}

    def _process_hits(
        self,
        response: dict,
        data: Dict[str, List[Dict]],
        seen_segments: Dict[str, Set[Tuple]]
    ) -> None:
        """Xử lý các hit từ Elasticsearch, lọc trùng segmentation"""
        hits = response.get("hits", {}).get("hits", [])

        for hit in hits:
            doc = hit["_source"]
            word = doc.get("word")
            if not word:
                continue

            seg_ipa = doc.get("segement_ipa", [])
            seg_word = doc.get("segement_word", [])

            if len(seg_ipa) != len(seg_word) or not seg_ipa:
                continue

            seg_ipa_tuple = tuple(seg_ipa)

            if seg_ipa_tuple in seen_segments[word]:
                continue

            item = {
                "ipa": doc.get("ipa", ""),
                "segement_ipa": seg_ipa,
                "segement_word": seg_word,
            }

            data[word].append(item)
            seen_segments[word].add(seg_ipa_tuple)