import eng_to_ipa
import pronouncing

# US

def convert_word_to_ipa(word):
    try:
        word_pron = eng_to_ipa.convert(word)
        if word_pron == word or '*' in word_pron:
            return None
        return word_pron
    except Exception:
        return None

def get_stress_pattern(word):
    """
    Args:
        word: str

    Returns:
        the stress position

    Explain:
        The function pronouncing.stresses_for_word returns a list where:
            1 indicates primary stress (main stress),
            2 indicates secondary stress,
            0 indicates no stress.
    """
    list_pattern = pronouncing.stresses_for_word(word)
    if list_pattern is None or list_pattern == []:
        return None
    pattern = list_pattern[0]
    if len(pattern) == 1:
        return None
    try:
        index = pattern.index('1') + 1
        return index
    except ValueError:
        return None


import random
from typing import Optional
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def transform_word(word: str) -> Optional[str]:
    """
    Transform a word into another word by changing its type, tense, article-related form,
    or meaning to create an incorrect answer for a 'find the wrong word' question.

    Args:
        word (str): The input word to transform.

    Returns:
        Optional[str]: The transformed word, or None if no transformation is possible.
    """
    # List of possible transformations
    transformation_methods = [
        transform_preposition,  # Handle prepositions
        transform_word_type,  # Change word type (e.g., noun to verb)
        transform_tense,  # Change verb tense
        transform_article,  # Change article-related form
        transform_meaning  # Change to a word with different meaning
    ]

    # Randomly select a transformation method
    random.shuffle(transformation_methods)
    for method in transformation_methods:
        transformed = method(word)
        if transformed and transformed != word:
            return transformed

    # Fallback: return a random word from nltk_words if no transformation works
    try:
        from src.factories.gen_question.base import nltk_words
        return random.choice(nltk_words) if nltk_words else None
    except ImportError:
        return None


def transform_preposition(word: str) -> Optional[str]:
    """
    Transform a preposition into another preposition that is likely to be incorrect in context.

    Args:
        word (str): The input word to check and transform.

    Returns:
        Optional[str]: A different preposition, or None if the input is not a preposition.
    """
    # Common prepositions and their common incorrect substitutions
    preposition_map = {
        'in': ['on', 'at', 'to'],
        'on': ['in', 'at', 'over'],
        'at': ['in', 'on', 'by'],
        'to': ['in', 'at', 'for'],
        'for': ['to', 'with', 'in'],
        'with': ['for', 'by', 'in'],
        'by': ['with', 'at', 'on'],
        'from': ['to', 'in', 'at'],
        'of': ['for', 'in', 'on']
    }

    word_lower = word.lower()
    if word_lower in preposition_map:
        return random.sample(preposition_map[word_lower], 1)[0]
    return None

def transform_word_type(word: str) -> Optional[str]:
    """
    Transform a word by changing its part of speech (e.g., noun to verb).
    Uses WordNet to find related words with different POS.
    """
    pos_map = {
        'n': 'v',  # Noun to verb
        'v': 'n',  # Verb to noun
        'a': 'r',  # Adjective to adverb
        'r': 'a'  # Adverb to adjective
    }

    # Get part of speech for the word
    synsets = wn.synsets(word)
    if not synsets:
        return None

    current_pos = synsets[0].pos()  # Get the first synset's POS
    target_pos = pos_map.get(current_pos)
    if not target_pos:
        return None

    # Find a synset with the target POS
    for synset in wn.synsets(word):
        if synset.pos() == target_pos:
            return synset.lemmas()[0].name().replace('_', ' ')

    return None


def transform_tense(word: str) -> Optional[str]:
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


def transform_article(word: str) -> Optional[str]:
    """
    Transform a word related to articles (e.g., 'a' to 'an' or remove article).
    For nouns, return a different noun that might cause article-related errors.
    """
    if word.lower() in ['a', 'an']:
        return 'an' if word.lower() == 'a' else 'a'

    # For nouns, find another noun that might cause article confusion
    synsets = wn.synsets(word, pos='n')
    if not synsets:
        return None

    # Pick a random synonym or related noun
    synonyms = []
    for synset in synsets:
        for lemma in synset.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym != word:
                synonyms.append(synonym)

    return random.sample(synonyms, 1)[0] if synonyms else None


def transform_meaning(word: str) -> Optional[str]:
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


