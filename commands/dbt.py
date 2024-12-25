import shlex

from commands.base import BaseCommand


class DbtCommand(BaseCommand):
    command = "dbt"
    imports = ["dbt.cli.main"]
    packages = ["dbt-core"]

    def run(self, line: str):
        from dbt.cli.main import dbtRunner

        runner = dbtRunner()
        runner.invoke(shlex.split(line))
