import json
from src.core.commands import Command


class SelectCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "select"

    @classmethod
    def description(cls) -> str:
        return "Select a client ID to target for commands: select <client_id>"

    @classmethod
    def is_server_side(cls) -> bool:
        return True

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        # Requires exactly one argument and it must be a valid integer (client ID)
        if len(args) != 1 or not args[0].isdigit():
            return False
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        """Returns the target client ID message."""
        server.id_asked = int(args[0])
        return None