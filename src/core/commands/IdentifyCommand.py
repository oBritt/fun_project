
from .Command import Command
import json
import platform

class IdentifyCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "identify"

    @classmethod
    def description(cls) -> str:
        return "Identify the client using its PC name"

    @classmethod
    def is_server_side(cls) -> bool:
        # Runs on the client side when requested by the server
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        """Turns CLI or input arguments into the wire JSON format."""
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        """
        Executed client-side: retrieves and returns the local machine's PC name.
        """
        pc_name = platform.node() or "Unknown-PC"
        return pc_name