from src.enums import QuestionTypeEnum
from src.factories.gen_question.types.antonym_question import AntonymsQuestion
from src.factories.gen_question.types.incorrect_word_question import IncorrectWordQuestion
from src.factories.gen_question.types.stress_question import StressQuestion
from src.factories.gen_question.types.synonym_question import SynonymsQuestion
from src.factories.gen_question.types.fill_in_blank_question import FillInBlankQuestion
from src.factories.gen_question.types.rearrange import RearrangenQuestion
from src.utils.exceptions import BadRequestException


def create_question_instance(type: QuestionTypeEnum, model_type = 'gemini') :
    if type == QuestionTypeEnum.PRONUNCIATION :
        return StressQuestion(model_type)
    elif type == QuestionTypeEnum.STRESS :
        return StressQuestion(model_type)
    elif type == QuestionTypeEnum.SYNONYM :
        return SynonymsQuestion(model_type)
    elif type == QuestionTypeEnum.ANTONYM :
        return AntonymsQuestion(model_type)
    elif type == QuestionTypeEnum.INCORRECT_WORD:
        return IncorrectWordQuestion(model_type)
    elif type == QuestionTypeEnum.FILL_IN_BLANK:
        return FillInBlankQuestion(model_type)
    elif type == QuestionTypeEnum.REARRANGE:
        return RearrangenQuestion(model_type)
    else:
        raise BadRequestException('type_invalid')