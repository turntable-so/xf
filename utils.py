import tomlkit


def get_version():
    with open("pyproject.toml", "r") as f:
        data = tomlkit.load(f)
    return data["project"]["version"]
