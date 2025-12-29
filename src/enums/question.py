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
    