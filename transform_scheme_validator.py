from __future__ import annotations
from settings_loader import TRANSFORM_SCHEME
from typing import Literal
from logger_logic import logg


def call_key_error(field: Literal["user", "group"]):
    raise KeyError(f"The mandatory field '{field}' is missing in 'transform_scheme'.")


@logg()
def validate_transform_scheme():
    if "user" not in TRANSFORM_SCHEME:
        call_key_error("user")
    if "group" not in TRANSFORM_SCHEME:
        call_key_error("group")


def scheme_injector(scheme: dict[str, str], injector_scheme: dict[str, str], scheme_type: Literal["user", "group"]):
    for key in injector_scheme:
        if key in scheme and scheme[key] != injector_scheme[key]:
            raise ValueError(f"System values are redefined in the {scheme_type} transformation schema."
                             f" Functional meanings: {injector_scheme[key]}")
        scheme[key] = injector_scheme[key]


def schemes_injector():
    user = {"Имя учетной записи пользователя": "name",
            "ipantsecurityidentifier": "sec_id",
            "Участник групп": "groups"}
    scheme_injector(TRANSFORM_SCHEME, user, "user")
    group = {"Имя группы": "name"}
    scheme_injector(TRANSFORM_SCHEME, group, "group")
