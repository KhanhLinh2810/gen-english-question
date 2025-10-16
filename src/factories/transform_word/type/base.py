from abc import  ABC, abstractmethod
from typing import Optional

class Word(ABC):
    @abstractmethod
    def transform_word(self, word: str) -> Optional[str]:
        pass
