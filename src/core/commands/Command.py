
from abc import abstractmethod, ABC


class Command(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, txt: str) -> bool:
        ...

    @classmethod
    @abstractmethod
    def execute(cls, args:list[str]):
        ...
