import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from typing import Optional

import random

from src.factories.transform_word.type.base import Word

class Meaning(Word):
    # need update nhận thêm câu để tạo từ incorrect cho hợp lý, ví dụ: correct là cat, câu là "The cat is in house", incorrect là dog thì không có ý nghĩa, incorrect nên là a train 
    
    def transform_word(self, word: str) -> Optional[str]:
        """
            Transform a word to another with a different meaning (e.g., homophone or unrelated word).
        """
        # Find a word with different meaning but the same POS
        synsets = wn.synsets(word)
        if not synsets:
            return None

        current_pos = synsets[0].pos()
        # Get all words with the same POS but different synsets
        different_words = []
        for synset in wn.all_synsets(pos=current_pos):
            for lemma in synset.lemmas():
                candidate = lemma.name().replace('_', ' ')
                if candidate != word and candidate not in different_words:
                    different_words.append(candidate)

        return random.sample(different_words, 1)[0] if different_words else None
