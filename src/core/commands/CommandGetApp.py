

import pygetwindow as gw

from .Command import Command

class CommandGetApps(Command):

    parse_word = "apps"

    @classmethod
    def parse(cls, txt: str) -> bool:
        args = txt.split(" ")
        if len(args) != 2:
            return False
        if args[0] != CommandGetApps.parse_word:
            return False
        return True

    @classmethod
    def execute(cls, args:list[str]):
        return [app for app in gw.getAllTitles() if app.strip()]