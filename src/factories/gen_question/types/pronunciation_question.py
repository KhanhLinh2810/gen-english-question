# import random
# from typing import Set, List
# from src.factories.gen_question.base import Question
# from src.enums.question import QuestionTypeEnum
# from collections import defaultdict
# import pronouncing
#
#
# class PronunciationQuestion(Question):
#     def generate_questions(self, list_words: List[str], num_questions: int = 1, num_ans_per_question: int = 4) :
#         result = []
#         list_unique_words = set(list_words)
#
#         num_word_in_list_per_question = self.cal_num_word_in_list_available_per_question(len(list_words), num_questions, num_ans_per_question)
#
#         for _ in range(num_questions) :
#             main_word = None
#             main_segment = None
#             main_pron = None
#             while main_word is None and len(list_words) > 0:
#                 main_word = random.choice(list_words)
#                 main_segment = self.extract_main_segment(main_word)
#                 main_pron, segment_pron = self.get_pronunciation_of_word_and_segment(main_word, main_segment)
#                 if main_pron is None or segment_pron is None :
#                     main_word = None
#                 list_words.remove(main_word)
#
#             question = main_segment
#             choices = [main_word]
#             explain = [f'{main_word} : {main_pron}']
#             similar_pron_words = []
#             different_pron_word = None
#
#             # random main_char trong main_word de lam tu so sanh phien am
#             # tim trong list_words co tu nao chua main_char sao cho phiên âm của các từ được tìm thấy là 1 từ có phiên âm khác, còn các từ còn lại có phiên âm giống nhau
#             # xoa cac tu duoc chon trong list_words
#
#             result.append({
#                 "question": "",
#                 "type": QuestionTypeEnum.PRONUNCIATION,
#                 "choices": choices,
#                 "answer": `index_of_choice`,
#                 "explain":
#             })
#
#     def get_pronunciation_of_word_and_segment(self, word: str, segment: str):
#         word_pron = None
#         word_segment = None
#         try:
#             p = pronouncing.phones_for_word(word)
#             if not p:
#                 return None, None
#             word_pron = p[0]
#         except Exception:
#             return None, None
#
#
#
#
#
#
#     def extract_main_segment(self, word: str) -> str:
#         """
#         Extracts a random phonetic segment (vowel, consonant, consonant cluster, diphthong, or common ending)
#         from the word, excluding the last segment unless it's the only option.
#         For example, 'pronunciation' can be segmented as:
#         - Individual: ['p', 'r', 'o', 'n', 'u', 'n', 'c', 'i', 'a', 't']
#         - Grouped: ['p', 'r', 'o', 'n', 'u', 'n', 'c', 'i', 'a', 'tion']
#         For example, 'phone' can be segmented as:
#         - Grouped: ['ph', 'o', 'n', 'e']
#         """
#         if not word or len(word) <= 2:
#             return word
#
#         word = word.lower()
#
#         # Define phonetic components
#         vowels = set('aeiou')
#         consonant_clusters = ['th', 'ph', 'sh', 'ch', 'wh', 'gh', 'sch', 'tr', 'sh', 's', 't', 'p']
#         diphthongs = ['ai', 'au', 'ei', 'eu', 'oi', 'ou', 'ui', 'ie', 'io', 'ea', 'ee', 'oa', 'oe']
#         common_endings = ['tion', 'sion', 'ing', 'ed', 'es']
#
#         # Step 1: Segment the word
#         segments = []
#         i = 0
#         while i < len(word):
#             # Check for common endings (e.g., 'tion')
#             matched_ending = False
#             for ending in common_endings:
#                 if word[i:].startswith(ending) and i + len(ending) <= len(word):
#                     segments.append(ending)
#                     i += len(ending)
#                     matched_ending = True
#                     break
#             if matched_ending:
#                 continue
#
#             # Check for consonant clusters (e.g., 'th', 'ph', 'sch')
#             matched_cluster = False
#             for cluster in consonant_clusters:
#                 if word[i:].startswith(cluster) and i + len(cluster) <= len(word):
#                     segments.append(cluster)
#                     i += len(cluster)
#                     matched_cluster = True
#                     break
#             if matched_cluster:
#                 continue
#
#             # Check for diphthongs (e.g., 'io')
#             matched_diphthong = False
#             for diph in diphthongs:
#                 if word[i:].startswith(diph) and i + len(diph) <= len(word):
#                     segments.append(diph)
#                     i += len(diph)
#                     matched_diphthong = True
#                     break
#             if matched_diphthong:
#                 continue
#
#             # Add single character (vowel or consonant)
#             if word[i].isalpha():
#                 segments.append(word[i])
#             i += 1
#
#         # Step 2: Filter valid segments (exclude the last segment if possible)
#         valid_segments = segments[:-1] if len(segments) > 1 else segments
#
#         # Step 3: If no valid segments, fall back to single characters
#         if not valid_segments:
#             valid_positions = [i for i in range(len(word) - 1) if word[i].isalpha()]
#             if not valid_positions:
#                 return ''
#             pos = random.choice(valid_positions)
#             return word[pos]
#
#         # Step 4: Randomly choose a segment
#         return random.choice(valid_segments)
#
#     def cal_num_word_in_list_available_per_question(self, len_list_words: int, num_questions: int = 1, num_ans_per_question: int = 4) -> int:
#         num_word_in_list_available_per_question = len_list_words // num_questions
#         return num_word_in_list_available_per_question if num_word_in_list_available_per_question < num_ans_per_question else num_ans_per_question
