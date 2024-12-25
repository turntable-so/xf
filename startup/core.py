import io
import os  # noqa: F401
from contextlib import redirect_stdout

import IPython
import rich
from IPython.core.magic import Magics, line_magic, magics_class
from startup.console import build_panel
from startup.shell_mode import interpret_as_shell

from commands import BaseCommand
from main import test

stream = io.StringIO()


ipython = IPython.get_ipython()
ipython.input_transformers_post.append(interpret_as_shell)
ipython.run_line_magic("load_ext", "autoreload")
ipython.run_line_magic("autoreload", "2")
ipython.run_line_magic("pprint", "0")
with redirect_stdout(stream):
    ipython.run_line_magic("automagic", "off")
ipython.run_line_magic("load_ext", "shell_mode")


# Set custom banner
build_panel()


@magics_class
class PytestMagics(Magics):
    for cls in BaseCommand.__subclasses__():
        try:
            cls._check_installed()
        except ImportError:
            continue

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
