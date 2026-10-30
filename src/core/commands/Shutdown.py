import asyncio
import json
from src.core.commands import Command


class ShutdownCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "shutdown"

    @classmethod
    def description(cls) -> str:
        return "Shut down the client computer: shutdown [delay_in_seconds]"

    @classmethod
    def is_server_side(cls) -> bool:
        return False

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
    async def execute(cls, args: list[str]) -> str:
        """Executed client-side: triggers the native Windows shutdown command."""
        delay = "0"
        if args and args[0].isdigit():
            delay = args[0]

        try:
            # Invokes native Windows shutdown (/s = shutdown, /t = timer in seconds)
            process = await asyncio.create_subprocess_exec(
                "shutdown", "/s", "/t", delay,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

            if delay == "0":
                return "Command executed: Shutting down computer immediately..."
            else:
                return f"Command executed: Computer will shut down in {delay} seconds."
        except Exception as e:
            return f"Failed to shut down computer: {str(e)}"