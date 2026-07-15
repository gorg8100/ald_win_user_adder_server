from typing import Literal
import os


def permission_error_call(path: str, mode: Literal["read", "write"]):
    raise PermissionError(f"The file at the path {path} cannot be used in {mode} mode.")


def validate_file(path: str, mode: Literal["read", "write"]):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at the path {path} was not found.")
    if not os.path.isfile(path):
        raise TypeError(f"The path {path} is not a file.")
    if mode == "read":
        if not os.access(path, os.R_OK):
            permission_error_call(path, mode)
    else:
        if not os.access(path, os.W_OK):
            permission_error_call(path, mode)



