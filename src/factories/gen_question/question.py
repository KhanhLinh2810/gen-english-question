from src.enum.question import QuestionTypeEnum
from src.factories.gen_question.antonym_question import AntonymsQuestion
from src.factories.gen_question.incorrect_word_question import IncorrectWordQuestion
from src.factories.gen_question.stress_question import StressQuestion
from src.factories.gen_question.synonym_question import SynonymsQuestion
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
    else:
        raise BadRequestException('type_invalid')