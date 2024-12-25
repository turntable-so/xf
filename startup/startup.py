import json
import os  # noqa: F401

import IPython
from IPython.core.magic import Magics, line_magic, magics_class

from commands import BaseCommand
from core.console import build_panel, list_available_commands
from core.magics import base_magics, build_custom_magics

# get env variables
shell_mode = os.getenv("SHELL_MODE", "true") == "true"
command_json = os.getenv("COMMAND_JSON", None)
if command_json:
    commands_dict = json.loads(command_json)
    included = commands_dict["included"]
    excluded = commands_dict["excluded"]
else:
    included = []
    excluded = []

# get ipython
ipython = IPython.get_ipython()


# build custom magics
@magics_class
class CustomMagics(Magics):
    pass


commands = []
for cls in BaseCommand.__subclasses__():
    instance = cls()
    c = instance.command
    if included and c not in included:
        continue
    if excluded and c in excluded:
        continue

    try:
        instance._check_installed()
    except ImportError:
        # Skip commands that can't be installed
        continue

    commands.append(c)

    @line_magic
    def inner(self, line):
        return type(instance)().run(line)

    inner.__name__ = c

    # Attach the newly created line magic to PytestMagics under c.command
    setattr(CustomMagics, c, inner)

# Set custom banner
build_panel(shell_mode)

# Set magics
base_magics(ipython, shell_mode)
commands = build_custom_magics(ipython, included, excluded)

ipython.register_magics(CustomMagics)

# List available commands
list_available_commands(commands)
