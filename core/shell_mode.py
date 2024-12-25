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


def to_magic(line):
    if line.startswith("pytest"):
        return True
    return False


def interpret_as_shell(lines):
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


def load_ipython_extension(ipython):
    """
    This function is called by IPython when loading the extension using:
    %load_ext shell_mode
    """
    ipython.input_transformers_post.append(interpret_as_shell)


def unload_ipython_extension(ipython):
    """
    This function is called by IPython when unloading the extension using:
    %unload_ext shell_mode
    """
    ipython.input_transformers_post.remove(interpret_as_shell)
