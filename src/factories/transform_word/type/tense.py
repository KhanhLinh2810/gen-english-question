from typing import Optional

from src.factories.transform_word.type.base import Word

class Tense(Word):
    def transform_word(self, word: str) -> Optional[str]:
        """
            Transform a verb by changing its tense (e.g., present to past).
            Uses simple rules for common verb forms.
            """
        # Simple past tense rules for regular verbs
        if word.endswith('e'):
            return word + 'd'  # e.g., love -> loved
        elif word.endswith('y') and word[-2] not in 'aeiou':
            return word[:-1] + 'ied'  # e.g., study -> studied
        elif word[-1] not in 'aeiou' and word[-2] not in 'aeiou':
            return word + 'ed'  # e.g., walk -> walked
        else:
            # Irregular verbs (small hardcoded list for simplicity)
            irregular = {
                'run': 'ran',
                'go': 'went',
                'see': 'saw',
                'write': 'wrote',
                'is': 'was',
                'are': 'were'
            }
            return irregular.get(word, None)