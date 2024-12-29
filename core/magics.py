import io
from contextlib import redirect_stdout

from IPython.core.magic import line_magic

from commands import BaseCommand
from core.shell_mode import interpret_as_shell


def base_magics(ipython, commands, shell_mode=True):
    ipython.run_line_magic("load_ext", "autoreload")
    ipython.run_line_magic("autoreload", "2")
    with redirect_stdout(io.StringIO()):
        ipython.run_line_magic("automagic", "off" if shell_mode else "on")
    if shell_mode:
        ipython.input_transformers_post.append(interpret_as_shell(commands))


def _make_helper(cls):
    def helper(self, line):
        return cls()._maybe_profiled_run(line)

    return helper


def populate_custom_magics(base_class, included, excluded, ipython):
    commands = []
    subclasses = BaseCommand.__subclasses__()
    for cls in subclasses:
        instance = cls()
        c = instance.command
        if included and c not in included:
            continue
        if excluded and c in excluded:
            continue

        try:
            instance._import_packages()
            instance.warm()
        except ImportError:
            # Skip commands that can't be installed
            continue

        commands.append(c)

        helper = _make_helper(cls)

        helper.__name__ = c
        magic = line_magic(helper)

        setattr(base_class, c, magic)

    if len(commands) == 1:
        ipython.set_next_input(f"{commands[0]} ")
    return commands
