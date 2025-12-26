# import random

# from typing import Optional

# from src.factories.transform_word.type.base import Word

# class Preposition(Word):
#     def transform_word(self, word: str) -> Optional[str]:
#         """
#             Transform a preposition into another preposition that is likely to be incorrect in context.

#             Args:
#                 word (str): The input word to check and transform.

#             Returns:
#                 Optional[str]: A different preposition, or None if the input is not a preposition.
#             """
#         # Common prepositions and their common incorrect substitutions
#         preposition_map = {
#             'in': ['on', 'at', 'to'],
#             'on': ['in', 'at', 'over'],
#             'at': ['in', 'on', 'by'],
#             'to': ['in', 'at', 'for'],
#             'for': ['to', 'with', 'in'],
#             'with': ['for', 'by', 'in'],
#             'by': ['with', 'at', 'on'],
#             'from': ['to', 'in', 'at'],
#             'of': ['for', 'in', 'on']
#         }

#         word_lower = word.lower()
#         if word_lower in preposition_map:
#             return random.sample(preposition_map[word_lower], 1)[0]
#         return None

