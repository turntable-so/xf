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


def main():
    # Get the directory containing the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    startup_path = os.path.join(current_dir, "startup.py")

    with open(startup_path, "r") as f:
        startup_script = f.read()
    os.system(f"ipython --InteractiveShellApp.exec_lines='''{startup_script}'''")
