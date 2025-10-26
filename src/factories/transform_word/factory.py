from src.enums.word import TransformWordType
from src.factories.transform_word.type.article import Article
from src.factories.transform_word.type.meaning import Meaning
from src.factories.transform_word.type.part_of_speech import PartOfSpeech
from src.factories.transform_word.type.preposition import Preposition
from src.factories.transform_word.type.tense import Tense
from src.utils.exceptions import BadRequestException


def transform_word_instance(transform_type: TransformWordType) :
    if transform_type == TransformWordType.ARTICLE :
        return Article()
    elif transform_type == TransformWordType.MEANING :
        return Meaning()
    elif transform_type == TransformWordType.PART_OF_SPEECH :
        return PartOfSpeech()
    elif transform_type == TransformWordType.PREPOSITION :
        return Preposition()
    elif transform_type == TransformWordType.TENSE:
        return Tense()
    else:
        raise BadRequestException('type_invalid')