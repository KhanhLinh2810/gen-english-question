from enum import Enum

class QuestionTypeEnum(str, Enum):
    PRONUNCIATION = "pronunciation" # phien am
    STRESS = "stress" # trong am
    SYNONYM = "synonym" # tu dong nghia
    ANTONYM = "antonym" # tu trai nghia
    INCORRECT_WORD = "incorrect_word"
    FILL_IN_BLANK = "fill_in_blank" # dien vao cho trong
    REARRANGE = "rearrange" # sap xep lai cau
    
    FACT = "paragraph_fact"
    MAIN_IDEA = "paragraph_main_idea"
    VOCAB = "paragraph_vocab"
    INFERENCE = "paragraph_inference"
    PURPOSE = "paragraph_purpose"

class ChoiceTypeEnum(str, Enum):
    SINGLE_CHOICE = "single-choice"
    MULTIPLE_CHOICE = "multiple-choice"

class ParagraphQuestionTypeEnum(str, Enum):
    FACT = "paragraph_fact"
    MAIN_IDEA = "paragraph_main_idea"
    VOCAB = "paragraph_vocab"
    INFERENCE = "paragraph_inference"
    PURPOSE = "paragraph_purpose"
    