from IPython import start_ipython

from core.styling import get_ipython_config


def base(shell, included, excluded):
    config = get_ipython_config(shell, included, excluded)
    return start_ipython(config=config)


if __name__ == "__main__":
    base(shell=True, included=[], excluded=[])
