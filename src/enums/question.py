from enum import Enum

from enum import IntEnum

class QuestionTypeEnum(IntEnum):
    # Nhóm câu hỏi đơn lẻ
    PRONUNCIATION = 1      # phien am
    STRESS = 2             # trong am
    SYNONYM = 3            # tu dong nghia
    ANTONYM = 4            # tu trai nghia
    INCORRECT_WORD = 5     
    FILL_IN_BLANK = 6      # dien vao cho trong
    REARRANGE = 7          # sap xep lai cau

    # Nhóm câu hỏi đọc hiểu (Paragraph)
    FACT = 21              
    MAIN_IDEA = 22         
    VOCAB = 23             
    INFERENCE = 24         
    PURPOSE = 25

class ChoiceTypeEnum(str, Enum):
    SINGLE_CHOICE = "single-choice"
    MULTIPLE_CHOICE = "multiple-choice"

class ParagraphQuestionTypeEnum(IntEnum):
    # Nhóm câu hỏi đọc hiểu (Paragraph)
    FACT = 21              
    MAIN_IDEA = 22         
    VOCAB = 23             
    INFERENCE = 24         
    PURPOSE = 25

class QuestionContentEnum(str, Enum):
    PRONUNCIATION = 'Choose the option whose underlined part is pronounced differently from the others.'
    STRESS = 'Choose the word whose primary stress is placed differently from the others.'
    SYNONYM = 'Choose the word that is closest in meaning to "{word}".'
    ANTONYM = 'Choose the word that is opposite in meaning to "{word}".'

VOWELS = [
    # Nguyên âm đơn
    "iː", "ɪ", "ʊ", "uː", "e", "ə", "ɜː", "ɔː", "ɒ", "ɔɪ",
    "æ", "ʌ", "ɑː", "aɪ", "aʊ",

    # Nguyên âm đôi
    "eɪ", "əʊ",
]

CHAR_TO_PHONEME = {
    "a": ["æ", "ə", "eɪ", "ɑː", "e", "ɪ", "ɒ", "ʊ", "ɔː", "ʌ"],
    "u": ["æ", "ə", "ɜː", "ɪ", "ʊ", "uː", "ɔː", "ʌ"],
    "au": ["æ", "ə", "ɑː", "ɒ", "ɔː", "aʊ", "ʌ"],
    "e": ["ə", "eɪ", "e", "iː", "ɜː", "ɪ", "ɒ"],
    "er": ["ə", "ɜː"],
    "o": ["ə", "ɑː", "ɪ", "ɒ", "əʊ", "ʊ", "uː", "ɔː", "ʌ"],
    "ar": ["ə", "ɑː", "ɔː"],
    "i": ["ə", "iː", "ɜː", "ɪ", "aɪ", "ʌ"],
    # "re": ["ə"],
    # "ure": ["ə"],
    "our": ["ə", "ɜː", "ɔː", "aʊ"],
    "ou": ["ə", "ɑː", "ɒ", "əʊ", "ʊ", "uː", "ɔː", "aʊ", "ʌ"],
    "ai": ["ə", "eɪ", "e", "ɪ"],
    "io": ["ə", "aɪ"],
    "y": ["ə", "iː", "ɪ", "aɪ"],
    "ue": ["ə", "uː"],
    # "iou": ["ə"],
    "ia": ["ə", "ɪ", "aɪ"],
    "ay": ["eɪ", "e", "iː"],
    # "aigh": ["eɪ"],
    "ea": ["eɪ", "ɑː", "e", "iː", "ɪ"],
    "eigh": ["eɪ", "aɪ"],
    "ey": ["eɪ", "iː"],
    "ei": ["eɪ", "e", "iː", "ɪ", "aɪ"],
    # "al": ["ɑː"],
    # "are": ["ɑː"],
    "ear": ["ɑː", "ɜː"],
    "oa": ["ɑː", "əʊ", "ɔː"],
    "ie": ["e", "iː", "aɪ"],
    # "ayo": ["e"],
    "ae": ["e", "iː"],
    "ee": ["iː", "ɪ"],
    # "eo": ["iː"],
    "ir": ["ɜː", "aɪ"],
    "or": ["ɜː", "ɔː"],
    # "ur": ["ɜː"],
    # "ere": ["ɜː"],
    # "igh": ["aɪ"],
    # "eye": ["aɪ"],
    # "ye": ["aɪ"],
    # "ho": ["ɒ"],
    "ow": ["ɒ", "əʊ", "aʊ"],
    # "oh": ["əʊ"],
    "ough": ["əʊ", "uː", "ɔː"],
    "oe": ["əʊ", "uː"],
    # "owe": ["əʊ"],
    # "oi": ["ɔɪ"],
    # "oy": ["ɔɪ"],
    "oo": ["ʊ", "uː", "ɔː", "ʌ"],
    # "oul": ["ʊ"],
    # "ew": ["uː"],
    # "ui": ["uː"],
    # "aw": ["ɔː"],
    # "ore": ["ɔː"],
    # "augh": ["ɔː"],
    # "oar": ["ɔː"],
    # "oor": ["ɔː"],
    # "hour": ["aʊ"],
    # "owre": ["aʊ"]
}

PHONEME_TO_CHAR = {
    "æ": ["a", "u", "au"],
    "ə": ["a", "e", "u", "er", "o", "ar", "i", "re", "ure", "our", "ou", "ai", "io", "y", "au", "ue", "iou", "ia"],
    "eɪ": ["a", "ai", "ay", "aigh", "ea", "eigh", "ey", "ei", "e"],
    "eə": ["e", "a", "air", "are", "ar", "ear", "ere", "eir", "ea", "ayo", "ai", "ay", "ei"],
    "ɑː": ["ar", "a", "al", "are", "au", "ear", "o", "ou", "ea", "oa"],
    "e": ["e", "ea", "ai", "ay", "a", "ie", "ayo", "ei", "ae"],
    "iː": ["ee", "e", "ea", "ey", "ie", "y", "eo", "i", "ei", "ay", "ae"],
    "ɜː": ["er", "ir", "or", "ur", "ear", "ere", "our", "i", "e", "u"],
    "ɪ": ["i", "e", "y", "a", "o", "u", "ai", "ea", "ee", "ia", "ei"],
    "aɪ": ["i", "ia", "igh", "y", "ei", "eigh", "eye", "ye", "ir", "ie", "ei", "io"],
    "ɒ": ["o", "a", "ho", "au", "ou", "ow", "e"],
    "əʊ": ["o", "ow", "oa", "oh", "ough", "oe", "ou", "owe"],
    "ɔɪ": ["oi", "oy"],
    "ʊ": ["oo", "u", "o", "oul", "ou", "a"],
    "uː": ["oo", "ew", "u", "o", "oe", "ou", "ue", "ui", "ough"],
    "ɔː": ["o", "or", "a", "ar", "au", "aw", "ore", "augh", "oar", "oor", "oo", "ough", "our", "ou", "oa", "u"],
    "aʊ": ["ou", "ow", "hour", "our", "owre", "au"],
    "ʌ": ["u", "o", "ou", "oo", "au", "a", "i"],
}
SILENT_GRAPHEMES = [
    "b", "c", "d", "g", "h", "k", "l", "n", "p", "s", "t", "w", "gh"
]

SUFFIX_RULES = {
    "s": ["s", "z"],
    "es": ["s", "z", "iz"],
    "ed": ["t", "d", "id"],
}

GRAPHEME_RULES = {
    "th": ["θ", "ð"],
    "ch": ["tʃ", "ʃ", "k"],
    "t":  ["t", "tʃ"],
    "d":  ["d", "dʒ"],
}  