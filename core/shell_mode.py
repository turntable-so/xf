MAGIC_PREFERRED = ["cd", "pip"]

SHELL_MODE_ENV = "SHELL_MODE"
COMMAND_JSON_ENV = "COMMAND_JSON"


def to_ignore(line):
    if not line:
        return True
    if line.startswith("%") or line.startswith("?") or line.startswith("!"):
        return True
    if line.startswith("run_command("):
        return True
    if line.startswith("ipython.run_line_magic("):
        return True
    if line.startswith("get_ipython().system("):
        return True
    if line == "exit()":
        return True
    return False


def interpret_as_shell(commands):
    def to_magic(line):
        if line.startswith("pytest"):
            return True
        for magic in MAGIC_PREFERRED:
            if line == magic or line.startswith(magic):
                return True
        for command in commands:
            if line.startswith(command):
                return True
        return False

    def helper(lines):
        """
        If the line doesn't start with '%', '?', or '!',
        turn it into get_ipython().system('...').
        """
        if not isinstance(lines, list):
            return lines

        # Skip empty lines or lines that already look like IPython commands
        new_lines = []
        for line in lines:
            line = line.strip()
            if to_ignore(line):
                new_lines.append(line)
            elif to_magic(line):
                if " " not in line:
                    command = line
                    arg_string = ""
                else:
                    command, arg_string = line.split(" ", 1)
                new_lines.append(f"ipython.run_line_magic('{command}', '{arg_string}')")
            else:
                new_lines.append(f"get_ipython().system('''{line}''')")
        return new_lines

    return helper
