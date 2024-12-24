import io
from contextlib import redirect_stdout

import IPython
from IPython.core.magic import register_line_magic

from main import test

ipython = IPython.get_ipython()
ipython.run_line_magic("load_ext", "autoreload")
ipython.run_line_magic("autoreload", "2")

# Set custom banner
print("\n")
print("╔════════════════════════════════════════════════════════╗")
print("║            Pytest-turbo IPython Environment            ║")
print("║--------------------------------------------------------║")
print("║ - use %pytest just as you would pytest in the terminal ║")
print("║ - autoreload is enabled                                ║")
print("║ - type %pytest --help for more options                 ║")
print("╚════════════════════════════════════════════════════════╝")
print("\n")


# register pytest line magic
@register_line_magic
def pytest(line):
    return test(line)


# force pytest to run once with collection only so everything is imported
print("Loading all imports...")
stream = io.StringIO()
with redirect_stdout(stream):
    test("--co")

# set up ipython to start with pytest line magic by default
ipython.set_next_input("%pytest ")
