from __future__ import annotations
from settings_loader import COMMANDS
from conditions_validator import condition_validator
from logger_logic import logg


def validate_command(command: dict):
    condition_validator(command["condition"])
    if "ctype" not in command:
        raise KeyError(f"Mandatory field 'ctype' is missing in the command:")
    commands_set = {"add_to_local_group"}
    if command["ctype"] not in commands_set:
        raise TypeError(f"There is no such command {command['ctype']}. Existing commands: {commands_set}")
    if command["ctype"] == "add_to_local_group":
        if "local_group" not in command:
            raise KeyError("The 'local_group' field is mandatory for the add_to_local_group command.")


@logg()
def validate_commands():
    for command in COMMANDS:
        validate_command(command)
