from .Command import Command
from .HelpCommand import HelpCommand
from .IdentifyCommand import IdentifyCommand
from .AppsCommand import AppsCommand
from .SelectCommand import SelectCommand
from .ClientsCommand import ClientsCommand
from .CloseCommand import CloseCommand
from .UpdateCommand import UpdateCommand

commands_dict: dict[str, Command] = {
    HelpCommand.name(): HelpCommand,
    IdentifyCommand.name(): IdentifyCommand,
    AppsCommand.name(): AppsCommand,
    SelectCommand.name(): SelectCommand,
    ClientsCommand.name(): ClientsCommand,
    CloseCommand.name(): CloseCommand,
    UpdateCommand.name(): UpdateCommand,
}

__all__ = [
    commands_dict,
    Command,
    HelpCommand,
    SelectCommand
]