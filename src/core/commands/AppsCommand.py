

import json
import pygetwindow as gw
from .Command import Command


class AppsCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "apps"

    @classmethod
    def description(cls) -> str:
        return "List open application windows on the client"

    @classmethod
    def is_server_side(cls) -> bool:
        # Executes client-side because it queries the local client machine's windows
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        # No special arguments needed to list apps
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        """Turns the command into the wire JSON format."""
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> list[str]:
        """Executed client-side: retrieves all non-empty active window titles."""
        return [app for app in gw.getAllTitles() if app.strip()]