from abc import ABC, abstractmethod


from src.interfaces.question import ICreateQuestionForParagraph

class Question(ABC):        
    @abstractmethod
    def generate_questions(self, data: ICreateQuestionForParagraph):
        pass