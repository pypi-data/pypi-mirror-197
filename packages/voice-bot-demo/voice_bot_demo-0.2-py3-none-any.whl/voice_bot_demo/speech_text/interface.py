from abc import ABC, abstractmethod
from typing import Callable


class SpeechTextInterface(ABC):
    @abstractmethod
    def run(self, device_index: int, process_sentence: Callable[[str], None]) -> None:
        raise NotImplementedError
