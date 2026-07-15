from __future__ import annotations
import functools
import time
from datetime import datetime
from typing import TypeVar, Callable
from settings_loader import DATA_LOGS_PATH
from info_raise import InfoRaise


def write_log(record_type: str, error: Exception, func_name: str):
    with InfoRaise(
            f"Error when opening a file to write to the log at the path {DATA_LOGS_PATH} with error {error} in {func_name}"):
        with open(DATA_LOGS_PATH, "a") as file:
            print("========================", file=file)
            print(
                f"[{datetime.now().replace(microsecond=0)}][{record_type}]{type(error).__name__}: {error}. In {func_name}.",
                file=file)


T = TypeVar("T")


def logg(repeat: int = 1, repeat_timer: float = None) -> Callable:
    if repeat < 1:
        raise RuntimeError('Repeat must be greater than 0')

    def decorator_logg(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            error = None
            for i in range(repeat):
                try:
                    original_result = func(*args, **kwargs)
                    return original_result
                except Exception as err:
                    if i != repeat - 1:
                        if repeat_timer:
                            time.sleep(repeat_timer)
                        write_log(record_type="RepeatError", error=err, func_name=func.__name__)
                    else:
                        error = err
            write_log(record_type="Error", error=error, func_name=func.__name__)
            raise error

        return wrapper

    return decorator_logg
