from IPython import get_ipython

from commands.base import TO_PROFILE_ENV, TO_PROFILE_HTML_ENV, BaseCommand
from utils.env import FALSE, TRUE, set_env


class ProfileCommand(BaseCommand):
    command = "prof"
    imports = ["pyinstrument"]
    packages = ["pyinstrument"]

    def run(self, line: str):
        save_html = False
        if " " in line:
            command_list = line.split(" ")
            if command_list[0] == "--html":
                save_html = True
                command_list.pop(0)
            command = " ".join(command_list)
        else:
            command = line

        with set_env(
            **{
                TO_PROFILE_ENV: TRUE,
                TO_PROFILE_HTML_ENV: TRUE if save_html else FALSE,
            }
        ):
            get_ipython().run_cell(command)
