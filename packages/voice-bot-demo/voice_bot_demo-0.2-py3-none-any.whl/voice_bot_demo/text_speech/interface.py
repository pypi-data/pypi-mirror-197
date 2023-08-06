from abc import ABC, abstractmethod


class TextSpeechInterface(ABC):
    @abstractmethod
    def process_sentence(self, text) -> None:
        raise NotImplementedError
