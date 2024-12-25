from pathlib import Path

from tomlkit import parse


def get_pyproject_path():
    return Path(__file__).parent.parent / "pyproject.toml"


def get_version():
    with open(get_pyproject_path(), "r") as f:
        data = parse(f.read())
    return data["project"]["version"]
