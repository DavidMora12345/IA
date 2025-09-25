from abc import ABC, abstractmethod

class TextEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
