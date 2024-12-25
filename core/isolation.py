import argparse
import json
import subprocess
from pathlib import Path

from IPython import start_ipython

from commands import BaseCommand
from core.styling import get_ipython_config
from utils.env import set_env


def base(shell, included, excluded):
    config = get_ipython_config(shell, included, excluded)
    with set_env(
        SHELL_MODE="true" if shell else "false",
        COMMAND_JSON=json.dumps({"included": included, "excluded": excluded}),
    ):
        return start_ipython(argv=[], config=config)


def get_imports_helper(included, excluded):
    imports = []
    for cls in BaseCommand.__subclasses__():
        instance = cls()
        if instance.command in included and instance.command not in excluded:
            imports.extend(instance.packages)
    return imports


def start(shell, included, excluded, isolate=False):
    if isolate:
        if not included and not excluded:
            raise ValueError(
                "You must include at least one command when using --isolated"
            )
        imports = get_imports_helper(included, excluded)
        invocation = ["uv", "run"]
        if imports:
            for import_name in imports:
                invocation.append("--with")
                invocation.append(import_name)

        invocation.extend(
            [
                "--isolated",
                str(Path(__file__).resolve()),
                json.dumps({"included": included, "excluded": excluded}),
                "--bypass",
            ]
        )
        if shell:
            invocation.append("--shell")
        subprocess.run(invocation)
    else:
        return base(shell, included, excluded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("commands_json", nargs="?", default="")
    parser.add_argument("--shell", action="store_true", default=False)
    parser.add_argument("--isolate", action="store_true", default=True)
    parser.add_argument("--bypass", action="store_true", default=False)
    args = parser.parse_args()
    if not args.commands_json:
        commands_dict = {"included": [], "excluded": []}
    else:
        commands_dict = json.loads(args.commands_json)
    if args.bypass:
        base(
            shell=args.shell,
            included=commands_dict.get("included", []),
            excluded=commands_dict.get("excluded", []),
        )
    else:
        start(
            shell=args.shell,
            included=commands_dict.get("included", []),
            excluded=commands_dict.get("excluded", []),
            isolate=args.isolate,
        )
