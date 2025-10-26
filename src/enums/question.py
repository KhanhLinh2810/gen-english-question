from enum import Enum

class QuestionTypeEnum(str, Enum):
    PRONUNCIATION = "pronunciation" # phien am
    STRESS = "stress" # trong am
    SYNONYM = "synonym" # tu dong nghia
    ANTONYM = "antonym" # tu trai nghia
    INCORRECT_WORD = "incorrect_word"
    FILL_IN_BLANK = "fill_in_blank" # dien vao cho trong
    REARRANGE = "rearrange" # sap xep lai cau

class ChoiceTypeEnum(str, Enum):
    SINGLE_CHOICE = "single-choice"
    MULTIPLE_CHOICE = "multiple-choice"