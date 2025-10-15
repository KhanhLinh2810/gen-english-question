from src.enum.question import QuestionTypeEnum
from src.utils.exceptions import BadRequestException


def get_question_type(question_type: QuestionTypeEnum) :
    if type == QuestionTypeEnum.SYLLABLE :
        return
    elif type == QuestionTypeEnum.STRESS :
        return
    elif type == QuestionTypeEnum.SYNONYM :
        return
    elif type == QuestionTypeEnum.ANTONYM :
        return
    else:
        raise BadRequestException('type_invalid')