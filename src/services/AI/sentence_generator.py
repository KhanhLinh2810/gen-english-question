from .base import Model
from typing import List
import random


class SentenceGeneratorModel(Model):
    """
    A wrapper around the base Model class to generate English sentences
    that include given vocabulary words.
    """

    _instance = None

    def __new__(cls, model_name: str = "google/flan-t5-base"):
        if cls._instance is None:
            cls._instance = super(SentenceGeneratorModel, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name: str = "google/flan-t5-base"):
        if self._initialized:
            return
        super().__init__(model_name)
        self._initialized = True

    def generate_sentence_from_words(
        self,
        vocab_list: List[str],
        min_words: int = 2,
        max_words: int = 5,
        model_max_length: int = 64,
        token_max_length: int = 64
    ) -> str:
        """
        Generate a sentence that uses the given vocabulary words.

        Args:
            vocab_list (List[str]): The list of available vocabulary words.
            min_words (int): Minimum number of words to include in sentence.
            max_words (int): Maximum number of words to include.
            model_max_length (int): Max length of generated sentence.
            token_max_length (int): Max length for tokenization.

        Returns:
            str: A generated sentence using selected words.
        """

        if not vocab_list:
            raise ValueError("vocab_list cannot be empty.")

        selected_words = random.sample(
            vocab_list, k=min(len(vocab_list), random.randint(min_words, max_words))
        )

        prompt = f"Write an English sentence using the following words: {', '.join(selected_words)}."

        sentence = self.inference(
            model_max_length=model_max_length,
            token_max_length=token_max_length,
            task=prompt
        )

        return sentence
