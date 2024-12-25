# XF

XF stands for extra fast. XF imports your key packages on first call, so you don't pay a recurring tax for imports. Usually saves 1-10 seconds per invocation after startup.

Key features
- Comes with two modes: ipython mode and shell mode. Ipython feels like an ipython console; shell operates like a terminal.
- Extensible: we will accept PRs for additional commands. See the `commands` directory for examples.
- Easily profile any command using the `prof` prefix.
- Can use your own environment or run in an isolated environment using the `--isolated` flag.

Who would benefit from this:
- You are a non-python developer using a python cli
- You are a python developer

Who would not benefit from this:
- Production use cases
- Long-running commands where a few seconds of savings don't make a difference
