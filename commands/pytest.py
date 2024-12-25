import io
import shlex
from contextlib import redirect_stdout

from commands.base import BaseCommand


class PytestCommand(BaseCommand):
    command = "pytest"
    imports = ["pytest"]
    packages = ["pytest"]

    def warm(self):
        with redirect_stdout(io.StringIO()):
            self.run("--collect")

    def _run(self, line: str):
        import pytest

        args = shlex.split(line)
        command = ["--rootdir", ".", *args]
        if "--create-db" not in args:
            command.append("--reuse-db")
            pytest.main(command)

    def run(self, line: str):
        try:
            from pytest_django.plugin import DjangoDbBlocker

            django_db_blocker = DjangoDbBlocker(_ispytest=True)
            with django_db_blocker.unblock():
                return self._run(line)
        except ImportError:
            return self._run(line)
