from __future__ import annotations
import json
import os
from info_raise import InfoRaise
from paths_validator import validate_file


def read_json_settings(file_path: str) -> dict:
    validate_file(file_path, "read")
    with InfoRaise(f"Error when opening a file to read the settings at the path {file_path}:"):
        with open(file_path, encoding="utf-8") as f:
            json_settings = json.load(f)
    return json_settings


def load_config(settings_path: str = "/etc/ald_win_user_adder_server_settings.json") -> tuple[
        str, str, dict,
        dict[str, dict[str, str]],
        list[dict]]:
    settings_path = os.environ.get("ALD_WIN_USER_ADDER_SERVER_SETTINGS_FILE_PATH", settings_path)
    if os.path.isfile(settings_path):
        json_settings = read_json_settings(settings_path)
    else:
        json_settings = read_json_settings("settings.json")
    if not {"log_file_path", "data_file_path", "transform_scheme", "commands"}.issubset(json_settings):
        raise RuntimeError("The settings file is not correct")
    return (json_settings["log_file_path"], json_settings["data_file_path"], json_settings["obj_filter"],
            json_settings["transform_scheme"], json_settings["commands"])


DATA_LOGS_PATH, DATA_FILE_PATH, OBJ_FILTER, TRANSFORM_SCHEME, COMMANDS = load_config()
validate_file(DATA_FILE_PATH, "write")
validate_file(DATA_LOGS_PATH, "write")
