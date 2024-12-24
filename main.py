import os
import shlex

import pytest as _pytest


def _pytest_helper(args_str, reuse_db=True):
    args = shlex.split(args_str)
    command = ["--rootdir", ".", *args]
    if reuse_db and "--create-db" not in args:
        command.append("--reuse-db")
    _pytest.main(command)


def test(args_str, reuse_db=True):
    try:
        from pytest_django.plugin import DjangoDbBlocker

        django_db_blocker = DjangoDbBlocker(_ispytest=True)
        with django_db_blocker.unblock():
            return _pytest_helper(args_str, reuse_db)
    except ImportError:
        return _pytest_helper(args_str, reuse_db)


from IPython import start_ipython
from IPython.terminal.prompts import Prompts, Token


class CustomPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [(Token.Prompt, "> ")]

    def continuation_prompt_tokens(self, cli=None, width=None):
        return [(Token.Prompt, "... ")]

    def out_prompt_tokens(self):
        return [(Token.Prompt, "")]


def main():
    from traitlets.config import Config

    config = Config()

    # Attach the custom prompt class
    config.TerminalInteractiveShell.prompts_class = CustomPrompt

    # Register custom magics when IPython starts
    parent = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(parent, "startup.py"), "r") as f:
        config.InteractiveShellApp.exec_lines = f.read()

    # Optionally, add other configurations here
    config.TerminalInteractiveShell.banner1 = ""
    config.TerminalInteractiveShell.banner2 = ""

    # Launch IPython with the custom configuration
    start_ipython(config=config)
