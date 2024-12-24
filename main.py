import os
import shlex
import subprocess

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
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython.terminal.prompts import Prompts, Token

TerminalInteractiveShell.colors = "Linux"


def get_short_cwd():
    """
    Returns the current working directory, shortened with '~' if in HOME.
    Example: /Users/you/Documents => ~/Documents
    """
    home = os.path.expanduser("~")
    cwd = os.getcwd()
    return cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd


def get_git_branch():
    """
    Returns the active Git branch name if inside a Git repo;
    returns an empty string if not in a Git repo.
    """
    try:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
        return branch
    except:
        return ""


def get_git_changes():
    """
    Returns the number of changed (including untracked) files in the repo.
    Uses `git status --porcelain` to get a list of changes.
    If not in a Git repo or something fails, returns 0.
    """
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
        )
        lines = output.decode("utf-8").strip().split("\n")
        # Filter out empty lines in case the output is empty
        lines = [l for l in lines if l.strip()]
        return len(lines)
    except:
        return 0


class Powerlevel10kStylePrompts(Prompts):
    """
    A custom IPython prompt style that shows:
      - Shortened path
      - Git branch
      - Number of Git changes as !N
      - A 'Powerlevel10k-like' arrow
      - IPython's In/Out numbering
    """

    def in_prompt_tokens(self, cli=None):
        short_cwd = get_short_cwd()
        branch = get_git_branch()
        num_changes = get_git_changes()

        tokens = []

        # Display the current directory
        tokens.append((Token.PromptDir, short_cwd))

        # If we're on a valid Git branch, display " on <branch> !N"
        if branch:
            tokens.append((Token.PromptSeparator, " on "))
            tokens.append((Token.PromptBranch, branch))
            if num_changes > 0:
                # Show "!N" only if there are changes
                tokens.append((Token.PromptChanges, f" !{num_changes}"))

        # Arrow-like symbol
        tokens.append((Token.PromptArrow, " ❯ "))

        # Standard IPython prompt bits
        tokens.append((Token.Prompt, "In ["))
        tokens.append((Token.PromptNum, str(self.shell.execution_count)))
        tokens.append((Token.Prompt, "]: "))

        return tokens

    def out_prompt_tokens(self):
        return [
            (Token.OutPrompt, "Out["),
            (Token.OutPromptNum, str(self.shell.execution_count)),
            (Token.OutPrompt, "]: "),
        ]


# Style the tokens:


def main():
    from traitlets.config import Config

    config = Config()

    # Attach the custom prompt class
    config.TerminalInteractiveShell.prompts_class = Powerlevel10kStylePrompts

    # Style overrides
    config.TerminalInteractiveShell.colors = "Linux"
    config.TerminalInteractiveShell.highlighting_style_overrides = {
        Token.PromptDir: "ansicyan",  # directory
        Token.PromptSeparator: "ansiblue",  # " on "
        Token.PromptBranch: "ansigreen",  # git branch
        Token.PromptChanges: "ansimagenta",  # the "!N" piece
        Token.PromptArrow: "ansiyellow",  # arrow symbol
    }

    # Register custom magics when IPython starts
    parent = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(parent, "startup.py"), "r") as f:
        config.InteractiveShellApp.exec_lines = f.read()

    # Optionally, add other configurations here
    config.TerminalInteractiveShell.banner1 = ""
    config.TerminalInteractiveShell.banner2 = ""

    # Launch IPython with the custom configuration
    start_ipython(config=config)
