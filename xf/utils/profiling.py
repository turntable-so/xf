import os
from functools import wraps

from pyinstrument.frame import Frame
from pyinstrument.frame_ops import delete_frame_from_tree
from pyinstrument.processors import ProcessorOptions
from pyinstrument.renderers.console import ConsoleRenderer
from pyinstrument.renderers.html import HTMLRenderer

XF_PATH = os.path.normpath("/site-packages/xf/")


# Define a custom filter to exclude frames from the "xf" module
def remove_xf(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    if frame is None:
        return None

    for child in frame.children:
        remove_xf(child, options=options)

        if child.file_path and XF_PATH in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


class CustomHTMLRenderer(HTMLRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preprocessors.append(remove_xf)

    def should_render_frame(self, frame: Frame) -> bool:
        if XF_PATH in frame.identifier:
            return False
        return super().should_render_frame(frame)


class CustomConsoleRenderer(ConsoleRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processors.append(remove_xf)

    def should_render_frame(self, frame: Frame) -> bool:
        if XF_PATH in frame.identifier:
            return False
        return super().should_render_frame(frame)

    def should_render_frame_in_group(self, frame: Frame) -> bool:
        if XF_PATH in frame.identifier:
            return False
        return super().should_render_frame_in_group(frame)


def pyprofile(show_all=False, save_html=False):
    from pyinstrument import Profiler

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = Profiler()
            profiler.start()

            try:
                result = func(*args, **kwargs)
            finally:
                profiler.stop()

                # Get the session and apply the custom filter
                if save_html:
                    session = profiler._get_last_session_or_fail()

                    return CustomHTMLRenderer(timeline=False).open_in_browser(session)
                else:
                    print(
                        profiler.output(
                            renderer=CustomConsoleRenderer(
                                show_all=show_all,
                                unicode=True,
                                color=True,
                            )
                        )
                    )

            return result

        return wrapper

    return decorator
