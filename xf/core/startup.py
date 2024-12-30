import json
import os  # noqa: F401

import IPython
from IPython.core.magic import Magics, magics_class

from xf.core.console import build_panel, list_available_commands
from xf.core.magics import base_magics, populate_custom_magics
from xf.core.shell_mode import COMMAND_JSON_ENV, SHELL_MODE_ENV
from xf.utils.env import TRUE

# get env variables
shell_mode = os.getenv(SHELL_MODE_ENV) == TRUE
command_json = os.getenv(COMMAND_JSON_ENV, {"included": [], "excluded": []})
commands_dict = json.loads(command_json)
included = commands_dict["included"]
excluded = commands_dict["excluded"]


# get ipython
ipython = IPython.get_ipython()


# Set custom banner
build_panel(shell_mode)


# Set custom magics
class MagicsBase:
    pass


commands = populate_custom_magics(MagicsBase, included, excluded, ipython)


@magics_class
class CustomMagics(MagicsBase, Magics):
    pass


ipython.register_magics(CustomMagics)

# Set base magics
base_magics(ipython, commands, shell_mode)

# List available commands
list_available_commands(commands)
