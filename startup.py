import io
from contextlib import redirect_stdout

import IPython
from IPython.core.magic import Magics, line_magic, magics_class

from main import test

ipython = IPython.get_ipython()
ipython.run_line_magic("load_ext", "autoreload")
ipython.run_line_magic("autoreload", "2")

# Set custom banner
print("\n")
print("╔════════════════════════════════════════════════════════╗")
print("║            Pytest-turbo IPython Environment            ║")
print("║--------------------------------------------------------║")
print("║ - use pytest just as you normally would                ║")
print("║ - autoreload is enabled                                ║")
print("╚════════════════════════════════════════════════════════╝")
print("\n")


@magics_class
class PytestMagics(Magics):
    @line_magic
    def pytest(self, line):
        return test(line)


ipython.register_magics(PytestMagics)


# force pytest to run once with collection only so everything is imported
print("Loading all imports...")
stream = io.StringIO()
with redirect_stdout(stream):
    test("--co")

# set up ipython to start with pytest line magic by default
ipython.set_next_input("pytest ")
