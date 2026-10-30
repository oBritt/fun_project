import json
from src.core.commands import Command


class ClientsCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "clients"

    @classmethod
    def description(cls) -> str:
        return "List all connected clients"

    @classmethod
    def is_server_side(cls) -> bool:
        return True

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        """Formats and returns the list of connected clients."""
        if not server or not server.connected_users:
            return "No clients connected."

        result = "Connected clients:\n"
        for user in server.connected_users:
            name = user.name if user.name else "Unnamed"
            result += f"  ID: {user.id} | Name: {name} | Address: {user.ws.remote_address}\n"
        return result.strip()