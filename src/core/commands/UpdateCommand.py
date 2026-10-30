import asyncio
import json
import os
import sys
from src.core.commands import Command


class UpdateCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "update"

    @classmethod
    def description(cls) -> str:
        return "Pull latest code from git and restart the client"

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
    async def execute(cls, args: list[str], server=None) -> str:
        """Runs git pull and schedules a self-restart for the client."""
        try:
            # Run git pull asynchronously
            process = await asyncio.create_subprocess_exec(
                "git", "pull",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            output = stdout.decode().strip() or stderr.decode().strip()

            if process.returncode != 0:
                return f"Git pull failed:\n{output}"

            # Schedule a delayed restart so the client can send the response back first
            async def restart_client():
                await asyncio.sleep(2)
                python = sys.executable
                # Restart using 'python -m src.client.client' plus any original CLI arguments
                os.execv(python, [python, "-m", "src.client.client"] + sys.argv[1:])

            asyncio.create_task(restart_client())

            return f"Git pull successful:\n{output}\n\nRestarting client..."

        except Exception as e:
            return f"Failed to update: {str(e)}"