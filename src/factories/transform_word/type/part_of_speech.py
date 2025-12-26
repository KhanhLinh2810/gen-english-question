# import nltk
# nltk.download('wordnet')
# from nltk.corpus import wordnet as wn

# from typing import Optional

# from src.factories.transform_word.type.base import Word

# class PartOfSpeech(Word):
#     def transform_word(self, word: str) -> Optional[str]:
#         """
#            Transform a word by changing its part of speech (e.g., noun to verb).
#            Uses WordNet to find related words with different POS.
#            """
#         pos_map = {
#             'n': 'v',  # Noun to verb
#             'v': 'n',  # Verb to noun
#             'a': 'r',  # Adjective to adverb
#             'r': 'a'  # Adverb to adjective
#         }

#         # Get part of speech for the word
#         synsets = wn.synsets(word)
#         if not synsets:
#             return None

#         current_pos = synsets[0].pos()  # Get the first synset's POS
#         target_pos = pos_map.get(current_pos)
#         if not target_pos:
#             return None

#         # Find a synset with the target POS
#         for synset in wn.synsets(word):
#             if synset.pos() == target_pos:
#                 return synset.lemmas()[0].name().replace('_', ' ')

#         return None