from pathlib import Path

from tomlkit import parse


def get_root_path():
    return Path(__file__).parent.parent


def get_main_path():
    return get_root_path() / "main.py"


def get_pyproject_path():
    return get_root_path() / "pyproject.toml"


def get_version():
    with open(get_pyproject_path(), "r") as f:
        data = parse(f.read())
    return data["project"]["version"]
