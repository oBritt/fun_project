import json
import pyttsx3
from src.core.commands import Command


class SpeakCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "say"

    @classmethod
    def description(cls) -> str:
        return "Make the client PC speak text out loud: say <message>"

    @classmethod
    def is_server_side(cls) -> bool:
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        return len(args) > 0

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        text = " ".join(args)
        try:
            # Initialize text-to-speech engine and speak out loud
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return f"Said aloud: '{text}'"
        except Exception as e:
            return f"Failed to speak: {str(e)}"