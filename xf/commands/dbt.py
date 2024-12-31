import shlex

from xf.commands.base import BaseCommand


class DbtCommand(BaseCommand):
    command = "dbt"
    imports = ["dbt.cli.main"]
    packages = ["dbt-core"]
    extras_required_in_isolation_mode = True

    def run(self, line: str):
        from dbt.cli.main import dbtRunner

        runner = dbtRunner()
        runner.invoke(shlex.split(line))
