import io
import warnings
from contextlib import redirect_stdout

from IPython.core.magic import Magics, line_magic, magics_class

from commands import BaseCommand
from core.shell_mode import interpret_as_shell


def base_magics(ipython, shell_mode=True):
    ipython.run_line_magic("load_ext", "autoreload")
    ipython.run_line_magic("autoreload", "2")
    with redirect_stdout(io.StringIO()):
        ipython.run_line_magic("automagic", "off" if shell_mode else "on")
    if shell_mode:
        ipython.input_transformers_post.append(interpret_as_shell)
        ipython.run_line_magic("load_ext", "shell_mode")


def build_custom_magics(ipython, included, excluded):
    @magics_class
    class PytestMagics(Magics):
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
            instance.check_installed()
        except ImportError:
            # Skip commands that can't be installed
            continue

        commands.append(c)

        @line_magic
        def pytest(self, line):
            return type(instance)().run(line)

        pytest.__name__ = c

        # Attach the newly created line magic to PytestMagics under c.command
        setattr(PytestMagics, c, pytest)

    breakpoint()

    ipython.register_magics(PytestMagics)

    if len(commands) == 0:
        warnings.warn("No commands found")
    elif len(commands) == 1:
        ipython.set_next_input(f"{commands[0]} ")

    return commands
