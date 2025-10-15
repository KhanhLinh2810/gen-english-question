from enum import Enum

class QuestionTypeEnum(str, Enum):
    PRONUNCIATION = "pronunciation" # phien am
    STRESS = "stress" # trong am
    SYNONYM = "synonym" # tu dong nghia
    ANTONYM = "antonym" # tu trai nghia
