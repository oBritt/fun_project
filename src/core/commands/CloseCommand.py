import json
import pygetwindow as gw
from src.core.commands import Command


class CloseCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "close"

    @classmethod
    def description(cls) -> str:
        return "Close an application window on the client: close <app_title>"

    @classmethod
    def is_server_side(cls) -> bool:
        # Executes on the client side to close a local window
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        # Requires at least an application title/name to close
        if not args:
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
        """Executed client-side: finds and closes the window matching the title."""
        title = " ".join(args)
        windows = gw.getWindowsWithTitle(title)

        if not windows:
            return f"Window not found: '{title}'"

        window = windows[0]
        window.close()
        return f"Successfully closed window: '{window.title}'"