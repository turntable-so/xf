import io
import os  # noqa: F401
from contextlib import redirect_stdout

import IPython
import rich
from IPython.core.magic import Magics, line_magic, magics_class
from rich import box
from rich.console import Console
from rich.panel import Panel
from startup.shell_mode import interpret_as_shell

from commands import BaseCommand
from main import test
from utils import get_version

stream = io.StringIO()


def run_command(command):
    os.system(command)


ipython = IPython.get_ipython()
ipython.input_transformers_post.append(interpret_as_shell)
ipython.run_line_magic("load_ext", "autoreload")
ipython.run_line_magic("autoreload", "2")
ipython.run_line_magic("pprint", "0")
with redirect_stdout(stream):
    ipython.run_line_magic("automagic", "off")
ipython.run_line_magic("load_ext", "shell_mode")


# Set custom banner
console = Console()
content = """\
[bright_green]•[/] use [bold bright_blue]pytest[/] just as you normally would
[bright_green]•[/] autoreload is enabled
[bright_green]•[/] general terminal commands will not work
[bright_green]•[/] type [bold]exit[/] to exit"""

panel = Panel(
    content,
    title="[bold orange1] Pytest-turbo IPython Environment[/]",
    subtitle=f"[dim]v{get_version()}[/]",  # Add a version or subtle note
    subtitle_align="right",  # Align subtitle to the right
    border_style="bright_cyan",
    box=box.DOUBLE,  # Try box.HEAVY, box.SQUARE, box.ROUNDED, etc.
    expand=False,  # Width matches content
    padding=(1, 2),  # Top/bottom = 1, left/right = 2
)

# Print the panel centered in the terminal
console.print(panel)


@magics_class
class PytestMagics(Magics):
    for cls in BaseCommand.__subclasses__():
        instance = cls()
        try:
            instance.check_installed()
        except ImportError:
            continue
        ipython.register_line_magic(instance.command, instance.run)

    @line_magic
    def pytest(self, line):
        return test(line)


ipython.register_magics(PytestMagics)


# force pytest to run once with collection only so everything is imported
rich.print("Loading imports, this may take a few seconds...")
with redirect_stdout(stream):
    test("--co")

# set up ipython to start with pytest line magic by default
ipython.set_next_input("pytest ")
