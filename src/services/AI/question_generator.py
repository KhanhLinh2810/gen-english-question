"""This module contains all tasks specific to question generation model

@Author: Karthick T. Sharma
"""

from .base import Model
from src.utils.text_process import postprocess_question


class QuestionGenerator(Model):
    """Generate question from context and answer."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuestionGenerator, cls).__new__(cls)
            cls._instance._init_model()
        return cls._instance

    def _init_model(self):
        """Initialize question generator once."""
        super().__init__(model_name='iarfmoose/t5-base-question-generator')

    # def __init__(self):
    #     """Initialize question generator."""
    #     super().__init__(model_name='iarfmoose/t5-base-question-generator')
        # super().__init__(model_name='t5-question',
        #                  path_id='1_0dPLdv8WNtSYQdKEWxFc03IR-szs0kB')

    def generate(self, context, answer):
        """Generate abstrative summary of given context.

        Args:
            context (str): input corpus.
            ans (str): ans for question that needs to be generated.

        Returns:
           str: generated question.
        """
        return postprocess_question(self().inference(
            num_beams=5, no_repeat_ngram_size=2, model_max_length=72,
            token_max_length=382, context=context, answer=answer))
