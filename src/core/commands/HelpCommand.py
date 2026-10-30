
from .Command import Command
import json

class HelpCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "help"

    @classmethod
    def description(cls) -> str:
        return "Show this help message"

    @classmethod
    def is_server_side(cls) -> bool:
        return True

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        return json.dumps({"action": cls.name(), "args": args})

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        """Generates the help output listing all registered server commands."""
        from src.core.commands import commands_dict
        help_text = "Available commands:\n"

        for name in commands_dict.keys():
            help_text += f"  {name} - {commands_dict[name].description()}\n"

        return help_text