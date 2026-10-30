
import subprocess
from src.core.commands import Command


class HackerCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "hacker"

    @classmethod
    def description(cls) -> str:
        return "Launch a green hacker-style CMD terminal"

    @classmethod
    def is_server_side(cls) -> bool:
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        import json
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        try:
            commands = [
                "color 2",
                "title SYSTEM DIAGNOSTICS",
                "echo Initializing system...",
                "ver",
                "systeminfo",
                "echo.",
                "ipconfig /all",
                "echo.",
                "arp -a",
                "echo.",
                "route print",
                "echo.",
                "tasklist",
                "echo.",
                "driverquery",
                "echo.",
                "netstat -ano",
                "echo.",
                "set",
                "echo.",
                "dir C:\\Windows\\System32 /s",
                "echo.",
                "tree C:\\Windows /f",
                "echo.",
                "echo SYSTEM ANALYSIS COMPLETE",
                "pause"
            ]

            script = " & ".join(commands)

            subprocess.Popen(
                ["cmd.exe", "/K", script],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            return "Hacker terminal launched."

        except Exception as e:
            return f"Failed to launch terminal: {e}"
