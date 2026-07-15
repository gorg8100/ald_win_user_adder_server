from __future__ import annotations
from my_functools import do_command
from logger_logic import logg
from settings_loader import TRANSFORM_SCHEME, OBJ_FILTER, COMMANDS
import unittest
from typing import Literal, Union
import json


@logg()
def parse_line(line: str) -> tuple[str, str]:
    sep = line.index(":")
    key = line[:sep]
    value = line[sep + 2:]
    return key, value


@logg()
def data_parser(data: list[str], scheme: dict[str, str], scheme_type: Literal["user", "group"]) -> list[dict[str, str]]:
    elements = []
    element = {}
    fields = set(scheme.values())
    for line in data:
        key, value = parse_line(line)
        element[scheme[key]] = value
        if fields.issubset(element):
            elements.append(element)
            element = {}
    if not len(elements):
        raise TypeError(
            f"It is impossible to retrieve any objects for a schema of type '{scheme_type}'. "
            f"Resulting fields: {element.keys()}. "
            f"Specified fields: {fields}")
    return elements


class ParsersTests(unittest.TestCase):
    def test_parse_line(self):
        line = "test field: test"
        self.assertEqual(parse_line(line), ('test field', 'test'))
        return

    def test_user_data_parser(self):
        users_data = ["dn: uid=admin",
                      "Имя учетной записи пользователя: admin",
                      "Link to department: ou=ald.company.lan",
                      "dn: uid=user",
                      "Имя учетной записи пользователя: user",
                      "Link to department: ou=ald.company.lan"
                      ]
        scheme = {
            "Имя учетной записи пользователя": "name",
            "dn": "dn",
            "Link to department": "ltd"
        }
        users = data_parser(users_data, scheme, "user")
        self.assertEqual(users, [{'dn': 'uid=admin', 'name': 'admin', 'ltd': 'ou=ald.company.lan'},
                                 {'dn': 'uid=user', 'name': 'user', 'ltd': 'ou=ald.company.lan'}])
        return


@logg()
def get_users_data(fields: list[str]) -> list[str]:
    return do_command(f'ipa user-find --sizelimit=0 --all | grep -E "{"|".join(fields)}"').split("\n")


@logg()
def user_formation() -> list[dict[str, Union[str, list[str]]]]:
    user_scheme: dict[str, str] = TRANSFORM_SCHEME["user"]
    users_data = get_users_data(list(user_scheme.keys()))
    users: list[dict[str, Union[str, list[str]]]] = data_parser(users_data, user_scheme, "user")
    for user in users:
        user["groups"] = list(map(lambda x: x[1:], user["groups"].split(",")))
    return users


@logg()
def get_groups_data(fields: list[str]) -> list[str]:
    return do_command(f'ipa group-find --sizelimit=0 --all | grep -E "{"|".join(fields)}"').split("\n")


@logg()
def group_formation() -> list[dict[str, str]]:
    group_scheme: dict[str, str] = TRANSFORM_SCHEME["group"]
    users_data = get_groups_data(list(group_scheme.keys()))
    return data_parser(users_data, group_scheme, "group")


@logg()
def data_formation() -> dict:
    return {"obj_filter": OBJ_FILTER, "users": user_formation(), "groups": group_formation(), "commands": COMMANDS}


@logg()
def write_data():
    with open('sw_templates.json', 'w') as f:
        f.write(json.dumps(data_formation()))
    return
