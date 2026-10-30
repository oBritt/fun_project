
from abc import ABC, abstractmethod
import json

class Command(ABC):

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """Unique command name/action identifier."""
        pass

    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """Description of what the command does."""
        pass

    @classmethod
    @abstractmethod
    def is_server_side(cls) -> bool:
        """
        Returns True if the command executes on the server side,
        or False if it executes on the client side.
        """
        pass

    @classmethod
    @abstractmethod
    def validate_args(cls, args: list[str]) -> bool:
        """
        Validates if the provided arguments are valid and match expected types
        (e.g., checking counts, numeric values like amounts).
        """
        pass

    @classmethod
    @abstractmethod
    def to_json(cls, args: list[str]) -> str:
        """
        Turns input/arguments into a JSON string to be sent over the wire.
        """
        pass

    @classmethod
    @abstractmethod
    async def execute(cls, args: list[str], server=None) -> str:
        """
        Executes the command logic and returns the result of the execution
        (e.g., returning a string or data payload).
        """
        pass