from __future__ import annotations
import subprocess
from typing import Union


def do_command(command: str, sudo: bool = False, inp: str = None, check_code: bool = True, ret_code: bool = False) -> \
        Union[str, tuple[int, str]]:
    if sudo:
        command = "sudo " + command
    result = subprocess.run(command, text=True, shell=True, input=inp, capture_output=True)
    if check_code and result.returncode != 0:
        raise RuntimeError(f"Command {command} failed, with exit code {result.returncode} and msg:\n{result.stderr}")
    if ret_code:
        return result.returncode, result.stdout
    else:
        return result.stdout
