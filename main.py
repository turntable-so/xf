from typing import Annotated

import typer

from core.isolation import start


def main(
    selection: Annotated[
        list[str] | None,
        typer.Argument(
            help="Select commands for your session. If not provided, all commands with available dependencies are included.",
        ),
    ] = None,
    exclude: Annotated[
        bool,
        typer.Option(
            "--exclude",
            "-x",
            help="By default, selected commands are included. Use this option to exclude them instead.",
            is_flag=True,
        ),
    ] = False,
    shell: Annotated[
        bool,
        typer.Option(
            "--shell",
            "-s",
            is_flag=True,
            help="In shell mode, commands are run through the shell by default, instead of the ipython console.",
        ),
    ] = False,
    isolate: Annotated[
        bool,
        typer.Option(
            "--isolate",
            "-i",
            help="Run the commands in an isolated environment using uvx. If using this option, you must explicitly select commands to include.",
            is_flag=True,
        ),
    ] = False,
):
    included = excluded = []
    if selection:
        if exclude:
            excluded = selection
        else:
            included = selection
    start(shell, included, excluded, isolate)


def go():
    typer.run(main)


if __name__ == "__main__":
    go()
