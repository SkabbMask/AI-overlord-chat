from abc import ABC, abstractmethod


class StorageBase(ABC):
    @abstractmethod
    def get_strategy(self, question_id: str) -> str:
        ...
