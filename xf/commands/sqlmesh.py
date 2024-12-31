import shlex

from xf.commands.base import BaseCommand


class SqlmeshCommand(BaseCommand):
    command = "sqlmesh"
    imports = ["sqlmesh.cli.main"]
    packages = ["sqlmesh"]
    extras_required_in_isolation_mode = True

    def run(self, line: str) -> None:
        from sqlmesh.cli.main import cli

        args = shlex.split(line)
        cli.main(args=args, standalone_mode=False)
