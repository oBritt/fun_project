from .Command import Command
from .BlueScreenCommand import BlueScreenCommand
from .HelpCommand import HelpCommand
from .IdentifyCommand import IdentifyCommand
from .AppsCommand import AppsCommand
from .SayCommand import SayCommand
from .SelectCommand import SelectCommand
from .ClientsCommand import ClientsCommand
from .CloseCommand import CloseCommand
from .UpdateCommand import UpdateCommand
from .HackerCommand import HackerCommand

commands_dict: dict[str, Command] = {
    HelpCommand.name(): HelpCommand,
    IdentifyCommand.name(): IdentifyCommand,
    AppsCommand.name(): AppsCommand,
    SelectCommand.name(): SelectCommand,
    ClientsCommand.name(): ClientsCommand,
    CloseCommand.name(): CloseCommand,
    UpdateCommand.name(): UpdateCommand,
    BlueScreenCommand.name(): BlueScreenCommand,
    HackerCommand.name(): HackerCommand,
    SayCommand.name(): SayCommand,
}

__all__ = [
    commands_dict,
    Command,
    HelpCommand,
    SelectCommand
]