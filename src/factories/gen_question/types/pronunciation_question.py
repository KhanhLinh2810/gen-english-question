import random
from typing import Set, List
from factories.gen_question_for_paragraph.types.base import Question
from loaders.elastic import Elastic
from src.enums.question import QuestionContentEnum, QuestionTypeEnum
from collections import defaultdict


class PronunciationQuestion(Question):

    vowels = [
        # Nguyên âm đơn
        "iː", "ɪ", "ʊ", "uː", "e", "ə", "ɜː", "ɔː", "ɒ", "ɔɪ",
        "æ", "ʌ", "ɑː", "aɪ", "aʊ",

        # Nguyên âm đôi
        "eɪ", "əʊ",
    ]

    silent_graphemes = [
        "b", "c", "d", "g", "h", "k", "l", "n", "p", "s", "t", "w", "gh"
    ]

    def generate_questions(self, list_words: List[str], num_questions: int = 1, num_ans_per_question: int = 4) :
        result = []
        list_unique_words = set(list_words)

        data, ipa_group = self.classify_type(list_unique_words)

        for _ in range(num_questions) :
            available_groups = list(ipa_group.keys())
            if not available_groups:
                continue
            
            if available_groups == "_s":
                result.append(self.create_question_for_suffix(ipa_group["_s"], list_unique_words, num_ans_per_question, "s", ["iz", "z", "s"]))
            elif available_groups == "_es":
                result.append(self.create_question_for_suffix(ipa_group["_es"], list_unique_words, num_ans_per_question, "es", ["iz", "z", "s"])) 
            elif available_groups == "_s":
                result.append(self.create_question_for_suffix(ipa_group["_ed"], list_unique_words, num_ans_per_question, "ed", ["id", "t", "d"]))

    def create_question_for_suffix(self, data_group, list_word, num_ans_per_question, suffix, list_different_ipa):
        answer_data = random.choice(data_group)
        
        # 2. Lấy IPA cuối cùng từ answer_data        
        segement_ipa = answer_data["segement_ipa"]        
        answer_ipa = segement_ipa[-1] 

        # 3. Chọn IPA khác biệt
        different_ipa = self.choice_different_ipa(list_different_ipa, answer_ipa)
        
        # 4. Tạo kết nối Elasticsearch
        es = Elastic()  
        
        # 5. Tạo query với script đúng cú pháp
        query = {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "script": {
                                "script": {
                                    "source": """
                                        // 1. Kiểm tra mảng có tồn tại và không rỗng
                                        if (doc['segement_word.keyword'].size() == 0 || doc['segement_ipa.keyword'].size() == 0) {
                                            return false;
                                        }
                                        
                                        // 2. Lấy độ dài mảng 
                                        int n = doc['segement_word.keyword'].size();
                                        int m = doc['segement_ipa.keyword'].size();
                                        
                                        // 3. Kiểm tra phần tử cuối cùng
                                        if (n > 0 && n == m) {
                                            String lastWordPart = doc['segement_word.keyword'][n-1];
                                            String lastIpaPart = doc['segement_ipa.keyword'][m-1];
                                            
                                            // Điều kiện: Chữ cái cuối là 's' VÀ phát âm cuối thỏa mãn
                                            return lastWordPart == params.suffix && lastIpaPart == params.different_ipa;
                                        }
                                        return false;
                                    """,
                                    "lang": "painless",
                                    "params": {
                                        "different_ipa": different_ipa,
                                        "suffix": suffix
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        def get_content_word(segement_word):
            content_choice = ""
            for i in range(len(segement_word)-1):
                content_choice += segement_word[i]
            return content_choice + "_" + suffix + "_"
                
        # 6. Thực hiện tìm kiếm
        try:
            response = es.search(
                index=self.INDEX,  
                body=query,
                size=num_ans_per_question * 3
            )

            used_word = set(answer_data["word"])
            choices = [
                {
                    "content": get_content_word(answer_data["word"]),
                    "is_correct": True,
                    "explaination": answer_data["ipa"]
                }
            ]
            
            # Xử lý kết quả
            hits = random.shuffle(response['hits']['hits'])
            for hit in hits:
                doc = hit['_source'] 
                if doc["word"] in used_word:
                    continue
                
                used_word.add(doc["word"])

                choices.append(
                    {
                        "content": get_content_word(doc["word"]),
                        "is_correct": False,
                        "explaination": doc["ipa"]
                    })
                
                if len(choices) == num_ans_per_question:
                    break
                
            return {
                "content": QuestionContentEnum.PRONUNCIATION,
                "type": QuestionTypeEnum.PRONUNCIATION,
                "choices": random.shuffle(choices)
            }     
            
        except Exception as e:
            print(f"Lỗi khi tìm kiếm Elasticsearch: {e}")
            return None

    def create_question(self, data_group, list_word, num_ans_per_question, char, list_different_ipa):
        answer_data = random.choice(data_group)
        
        # 2. Lấy IPA tương ứng với char       
        segement_ipa = answer_data["segement_ipa"] 
        segement_word = answer_data["segement_word"] 
        answer_ipa = None       
        for i in range(len(segement_word)):
            if segement_word[i] == char:
                answer_ipa = segement_ipa[i]
                break

        if answer_ipa is None:
            return None
        
        # 3. Chọn IPA khác biệt
        different_ipa = self.choice_different_ipa(list_different_ipa, answer_ipa)
        
        # 4. Tạo kết nối Elasticsearch
        es = Elastic()  
        
        # 5. Tạo query với script đúng cú pháp
        query = {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "script": {
                                "script": {
                                    "source": """
                                        // 1. Kiểm tra mảng có tồn tại và không rỗng
                                        if (doc['segement_word.keyword'].size() == 0 || doc['segement_ipa.keyword'].size() == 0) {
                                            return false;
                                        }
                                        
                                        // 2. Lấy độ dài mảng 
                                        int n = doc['segement_word.keyword'].size();
                                        int m = doc['segement_ipa.keyword'].size();
                                        
                                        // 3. Kiểm tra các phần tử trong ipa
                                        if (n < 0 || n != m) {
                                            return false;
                                        }
                                        for (int i=0, i<n, i++) {
                                            String wordPart = doc['segement_word.keyword'][n-1];
                                            String ipaPart = doc['segement_ipa.keyword'][m-1];
                                                
                                            if(wordPart == params.char && ipaPart == params.different_ipa)
                                                return true;
                                        }
                                        return false
                                    """,
                                    "lang": "painless",
                                    "params": {
                                        "different_ipa": different_ipa,
                                        "char": char
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        def get_content_word(segement_word, char):
            content_choice = ""
            for i in range(len(segement_word)):
                if segement_word[i] == char:
                    content_choice += "_" + char + "_"
                else:
                    content_choice += char

            return content_choice
                
        # 6. Thực hiện tìm kiếm
        try:
            response = es.search(
                index=self.INDEX,  
                body=query,
                size=num_ans_per_question * 4
            )

            used_word = set(answer_data["word"])
            choices = [
                {
                    "content": get_content_word(answer_data["word"], char),
                    "is_correct": True,
                    "explaination": answer_data["ipa"]
                }
            ]
            
            # Xử lý kết quả
            hits = random.shuffle(response['hits']['hits'])
            for hit in hits:
                doc = hit['_source'] 
                if doc["word"] in used_word:
                    continue
                
                used_word.add(doc["word"])

                choices.append(
                    {
                        "content": get_content_word(doc["word"], char),
                        "is_correct": False,
                        "explaination": doc["ipa"]
                    })
                
                if len(choices) == num_ans_per_question:
                    break
                
            return {
                "content": QuestionContentEnum.PRONUNCIATION,
                "type": QuestionTypeEnum.PRONUNCIATION,
                "choices": random.shuffle(choices)
            }     
            
        except Exception as e:
            print(f"Lỗi khi tìm kiếm Elasticsearch: {e}")
            return None

        

    def classify_type(self, list_words: List[str]):
        ipa_group = {
            "_s": [],
            "_es": [],
            "_ed": [],
            "silent": [],
            "th": [],
            "ch": [],
            "t": [],
            "d": [],
            # "_s_": [], 
        }
        
        data = self.fetch_phonetic_data_batch(list_words=list_words)
        for word in data:
            for data_ipa in word:
                saved_ipa = {
                    **data_ipa,
                    "word": word
                }
                seg_ipa = data_ipa["segement_ipa"]
                seg_word = data_ipa["segement_word"]
                n = len(seg_ipa)
                
                end_char = seg_word[n-1]
                if end_char == "s":
                    ipa_group["_s"].append(saved_ipa)
                elif end_char == "es":
                    ipa_group["_es"].append(saved_ipa)
                elif end_char == "ed":
                    ipa_group["_ed"].append(saved_ipa)

                for i in range(n):
                    if seg_word[i] == "th":
                        ipa_group["th"].append(saved_ipa)
                    if seg_word[i] == "ch":
                        ipa_group["ch"].append(saved_ipa)
                    if seg_word[i] == "t":
                        ipa_group["t"].append(saved_ipa)
                    if seg_word[i] == "d":
                        ipa_group["d"].append(saved_ipa)
                    # if seg_word[i] == "s" and i != n:
                    #     ipa_group["s"].append(saved_ipa)
                    if seg_word[i] in self.silent_graphemes and seg_ipa[i] == "":
                        ipa_group["silent"].append(saved_ipa)
        ipa_group = {k: v for k, v in ipa_group.items() if len(v) > 0}
        return data, ipa_group



    def fetch_phonetic_data_batch(self, list_words: List[str]):
        """
        Lấy dữ liệu IPA và phân đoạn (segmentation) từ Elasticsearch theo danh sách từ.
        Đảm bảo mỗi nhóm phân đoạn (segement_ipa) là duy nhất cho mỗi từ.
        """
        es = Elastic()  
        # data: Lưu kết quả cuối cùng theo cấu trúc { word: [items] }
        data = defaultdict(list) 
        seen_segments = defaultdict(set) 

        query = {
            "bool": {
                "must": [
                    {"terms": {"word": list_words}},
                    {"exists": {"field": "ipa"}},
                    {"exists": {"field": "stress"}}
                ]
            }
        }
        
        resp = es.search(
            index=self.INDEX,
            query=query,
            size=len(list_words) * 5
        )

        hits = resp["hits"].get("hits", [])

        for hit in hits:
            doc = hit["_source"]
            word = doc["word"]
            seg_ipa = doc.get("segement_ipa")
            seg_word = doc.get("segement_word")
            seg_ipa_tuple = tuple(seg_ipa) if isinstance(seg_ipa, list) else seg_ipa

            # Nếu segement_ipa đã tồn tại cho từ này thì bỏ qua để tránh trùng lặp
            if seg_ipa_tuple in seen_segments[word] or len(seg_word) != len(seg_ipa):
                continue
            
            item = {
                "ipa": doc.get("ipa"),
                "segement_ipa": seg_ipa,
                "segement_word": seg_word
            }
            
            data[word].append(item)
            seen_segments[word].add(seg_ipa_tuple)

        return dict(data)
    

    def choice_different_ipa(self, list_different_ipa: List[str], answer_ipa: str) -> str:
        different_ipas = [ipa for ipa in list_different_ipa if ipa != answer_ipa]
        
        if not different_ipas:
            return None
        
        # Chọn ngẫu nhiên 1 IPA từ danh sách
        return random.choice(different_ipas)



