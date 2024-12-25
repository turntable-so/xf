import os
import subprocess

from IPython.terminal.prompts import Prompts, Token
from traitlets.config import Config


def get_short_cwd():
    """
    Returns the current working directory, shortened with '~' if in HOME.
    Example: /Users/you/Documents => ~/Documents
    """
    home = os.path.expanduser("~")
    cwd = os.getcwd()
    if cwd.startswith(home):
        return cwd.replace(home, "~", 1)
    return cwd


def stylize_cwd_bold_last(path):
    from IPython.terminal.prompts import Token

    """
    Splits the path on '/' and creates two tokens:
      - everything except the last component, normal
      - last component, bold
    """
    if path == "~":
        # If the path is literally just "~", treat it all as last
        return [(Token.PromptDirBold, "~")]

    parts = path.split("/")
    # If there's only one element in parts, that's the final directory
    if len(parts) == 1:
        return [(Token.PromptDirBold, parts[0])]

    # Otherwise, join all but the last piece with '/'
    prefix = "/".join(parts[:-1])
    last = parts[-1]
    tokens = []
    # Include prefix plus a slash if prefix isn’t empty
    if prefix:
        tokens.append((Token.PromptDir, prefix + "/"))
    tokens.append((Token.PromptDirBold, last))

    return tokens


def get_git_branch():
    """
    Returns the active Git branch name if inside a Git repo;
    returns an empty string if not in a Git repo.
    """
    try:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
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
    """
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
        )
        lines = output.decode("utf-8").strip().split("\n")
        lines = [l for l in lines if l.strip()]
        return len(lines)
    except:
        return 0


class Powerlevel10kStylePrompts(Prompts):
    """
    A custom IPython prompt style that shows:
      - Shortened path (with final directory in bold)
      - Git branch
      - Number of Git changes as !N
      - A 'Powerlevel10k-like' arrow
      - IPython's In/Out numbering
    """

    def in_prompt_tokens(self, cli=None):
        short_cwd = get_short_cwd()
        stylized_cwd_tokens = stylize_cwd_bold_last(short_cwd)

        branch = get_git_branch()
        num_changes = get_git_changes()

        tokens = []

        # (1) Path tokens (with last directory bold)
        tokens.extend(stylized_cwd_tokens)

        # (2) If in a Git repo, show " on <branch> !N" if there are changes
        if branch:
            tokens.append((Token.PromptSeparator, " on "))
            tokens.append((Token.PromptBranch, branch))
            if num_changes > 0:
                tokens.append((Token.PromptChanges, f" !{num_changes}"))

        # (3) Arrow icon
        tokens.append((Token.PromptArrow, " ❯ "))

        return tokens

    def out_prompt_tokens(self):
        return []


# Style the tokens:
#   - PromptDir: normal color for the initial part of the path
#   - PromptDirBold: same color but bold for the last part
#   - Adjust these as you like. You can use "ansixxx" or "fg/bg:#xxxxxx bold" etc.
HIGHLIGHTING_STYLE_OVERRIDES = {
    Token.PromptDir: "ansicyan",  # normal path
    Token.PromptDirBold: "ansicyan bold",  # final directory in bold
    Token.PromptSeparator: "ansiblue",  # " on "
    Token.PromptBranch: "ansigreen",  # git branch
    Token.PromptChanges: "ansimagenta",  # !N if changed
    Token.PromptArrow: "ansiyellow",  # arrow symbol
}


def get_startup_contents(shell_mode=True, included=[], excluded=[]):
    parent = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(parent, "startup.py"), "r") as f:
        base_contents = f.read()

    base_contents += "\nmain("
    if included:
        base_contents += f"included={repr(included)}, "
    if excluded:
        base_contents += f"excluded={repr(excluded)}, "
    if shell_mode:
        base_contents += "shell_mode=True"
    else:
        base_contents += "shell_mode=False"
    base_contents += ")"

    return base_contents


def get_ipython_config(shell_mode=True, included=[], excluded=[]):
    config = Config()

    # Attach the custom prompt class
    if shell_mode:
        config.TerminalInteractiveShell.prompts_class = Powerlevel10kStylePrompts
        config.TerminalInteractiveShell.highlighting_style_overrides = (
            HIGHLIGHTING_STYLE_OVERRIDES
        )

    # Other styling
    config.TerminalInteractiveShell.banner1 = ""
    config.TerminalInteractiveShell.banner2 = ""

    # Register custom magics when IPython starts
    config.InteractiveShellApp.exec_lines = get_startup_contents(shell_mode)

    return config

    # Launch IPython with the custom configuration
    # start_ipython(config=config)
