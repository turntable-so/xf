import os  # noqa: F401

import IPython

from core.console import build_panel, list_available_commands
from core.magics import base_magics, build_custom_magics


def main(shell_mode=True, included=[], excluded=[]):
    ipython = IPython.get_ipython()

    # Set custom banner
    build_panel(shell_mode)

    # Set magics
    base_magics(ipython, shell_mode)
    commands = build_custom_magics(ipython, included, excluded)

    # List available commands
    list_available_commands(commands)
