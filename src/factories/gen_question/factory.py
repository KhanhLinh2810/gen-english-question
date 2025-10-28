from src.enums import QuestionTypeEnum
from src.factories.gen_question.types.antonym_question import AntonymsQuestion
from src.factories.gen_question.types.incorrect_word_question import IncorrectWordQuestion
from src.factories.gen_question.types.stress_question import StressQuestion
from src.factories.gen_question.types.synonym_question import SynonymsQuestion
from src.factories.gen_question.types.fill_in_blank_question import FillInBlankQuestion
from src.factories.gen_question.types.rearrange import RearrangenQuestion
from src.utils.exceptions import BadRequestException


def create_question_instance(question_type: QuestionTypeEnum) :
    if question_type == QuestionTypeEnum.PRONUNCIATION :
        return StressQuestion()
    elif question_type == QuestionTypeEnum.STRESS :
        return StressQuestion()
    elif question_type == QuestionTypeEnum.SYNONYM :
        return SynonymsQuestion()
    elif question_type == QuestionTypeEnum.ANTONYM :
        return AntonymsQuestion()
    elif question_type == QuestionTypeEnum.INCORRECT_WORD:
        return IncorrectWordQuestion()
    elif question_type == QuestionTypeEnum.FILL_IN_BLANK:
        return FillInBlankQuestion()
    elif question_type == QuestionTypeEnum.REARRANGE:
        return RearrangenQuestion()
    else:
        raise BadRequestException('type_invalid')