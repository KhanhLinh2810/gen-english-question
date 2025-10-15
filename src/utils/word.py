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
    pattern = list_pattern[0]
    try:
        index = pattern.index('1')
        return index
    except ValueError
        return None


