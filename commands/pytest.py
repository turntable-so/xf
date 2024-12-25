import io
import shlex
from contextlib import redirect_stdout

from commands.base import BaseCommand


class PytestCommand(BaseCommand):
    command = "pytest"

    def check_installed(self):
        import pytest  # noqa

    def start(self):
        with redirect_stdout(io.StringIO()):
            self.run("--collect")

    def run(self, args_str: str):
        import pytest

        args = shlex.split(args_str)
        command = ["--rootdir", ".", *args]
        if "--create-db" not in args:
            command.append("--reuse-db")
            pytest.main(command)
