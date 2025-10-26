from typing import List

from .base import Model
from src.enums import ChoiceTypeEnum
from src.llms.prompts import GEN_INCORRECT_WORD_QUESTION_PROMPT


class GemmaModel(Model):
    """Generalized text generation model (compatible with Gemma / GPT-style models)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GemmaModel, cls).__new__(cls)
            cls._instance._init_model()
        return cls._instance
    
    def _init_model(self):
        super().__init__(model_name="google/gemma-2b-it", device=None)

    def generate(self, list_words: List[str], question_type: ChoiceTypeEnum, num_ans_per_question: int = 4) -> str:
        """Tạo câu hỏi trắc nghiệm từ danh sách từ và loại câu hỏi.

        Args:
            list_words (List[str]): Danh sách các từ để tạo câu hỏi.
            question_type (ChoiceTypeEnum): Loại câu hỏi trắc nghiệm.
            num_ans_per_question (int): Số lượng lựa chọn cho mỗi câu hỏi (mặc định là 4).

        Returns:
            str: Câu hỏi được sinh ra.

        Raises:
            ValueError: Nếu danh sách từ rỗng hoặc số lượng lựa chọn không hợp lệ.
        """
        if not list_words:
            raise ValueError("Danh sách từ không được rỗng.")
        if num_ans_per_question < 2:
            raise ValueError("Số lượng lựa chọn phải lớn hơn hoặc bằng 2.")

        prompt = GEN_INCORRECT_WORD_QUESTION_PROMPT.format(
            list_of_words=", ".join(list_words),
            question_type=question_type.value,
            num_choices=num_ans_per_question
        )

        try:
            return self.inference(
                prompt,
                num_beams=4,
                no_repeat_ngram_size=2,
                model_max_length=128,
                num_return_sequences=1,
                token_max_length=256,
            )
        except Exception as e:
            raise RuntimeError(f"Lỗi khi sinh câu hỏi: {e}")