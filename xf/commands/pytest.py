import io
import shlex
from contextlib import redirect_stdout

from xf.commands.base import BaseCommand


class PytestCommand(BaseCommand):
    command = "pytest"
    imports = ["pytest"]
    packages = ["pytest"]

    def warm(self):
        with redirect_stdout(io.StringIO()):
            self.run("--co")

    def run(self, line: str):
        import pytest

        args = shlex.split(line)
        command = ["--rootdir", ".", *args]

        try:
            from pytest_django.plugin import DjangoDbBlocker

            if "--create-db" not in args:
                command.append("--reuse-db")

            django_db_blocker = DjangoDbBlocker(_ispytest=True)

            with django_db_blocker.unblock():
                return pytest.main(command)
        except ImportError:
            return pytest.main(command)
