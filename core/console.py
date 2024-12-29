import rich
from rich import box
from rich.console import Console
from rich.panel import Panel

from utils.paths import get_version


def build_panel(shell_mode=False):
    console = Console()
    content = "[bright_green]•[/] use commands just as you normally would"
    if shell_mode:
        content += "\n[bright_green]•[/] you're in [bold bright_blue]shell[/] mode. All terminal commands will work."
        content += "\n[bright_green]•[/] autoreload and automagic is enabled"

    else:
        content += "\n[bright_green]•[/] You're in [bold bright_blue]default[/] mode. General terminal commands will not work, prompt is ipython repl."
    content += "\n[bright_green]•[/] type [bold bright_blue]exit[/] to exit"

    if shell_mode:
        title = "[bold orange1] XF Shell Environment[/]"
    else:
        title = "[bold orange1] XF IPython Environment[/]"

    panel = Panel(
        content,
        title=title,
        subtitle=f"[dim]v{get_version()}[/]",  # Add a version or subtle note
        subtitle_align="right",  # Align subtitle to the right
        border_style="bright_cyan",
        box=box.DOUBLE,  # Try box.HEAVY, box.SQUARE, box.ROUNDED, etc.
        expand=False,  # Width matches content
        padding=(1, 2),  # Top/bottom = 1, left/right = 2
    )

    console.print(panel)
    console.print("Loading imports, this may take a few seconds...")


def list_available_commands(commands):
    if len(commands) == 0:
        rich.print("[bold red]No commands found[/]")
    else:
        rich.print(f"Available commands: {commands}")
