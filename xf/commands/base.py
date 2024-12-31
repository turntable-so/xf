import os

from xf.utils.env import TRUE
from xf.utils.profiling import pyprofile

TO_PROFILE_ENV = "XF_PROFILING"
TO_PROFILE_HTML_ENV = "XF_PROFILING_SAVE_HTML"


class BaseCommand:
    command: str
    imports: list[str]
    packages: list[str]

    # True if command requires extra imports in isolation mode
    extras_required_in_isolation_mode: bool = False

    def _import_packages(self):
        for import_name in self.imports:
            __import__(import_name)

    def warm(self):
        pass

    def run(self, line: str):
        pass

    def _maybe_profiled_run(self, line: str):
        if os.getenv(TO_PROFILE_ENV) == TRUE:

            @pyprofile(save_html=os.getenv(TO_PROFILE_HTML_ENV) == TRUE)
            def run(line: str):
                return self.run(line)

            return run(line)
        return self.run(line)

    @classmethod
    def get_command(cls, command: str):
        for command_class in cls.__subclasses__():
            if command_class.command == command:
                return command_class
        raise ValueError(f"Command {command} not found")
