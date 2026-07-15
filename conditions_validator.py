from __future__ import annotations
from typing import Type
from abc import ABC
from settings_loader import TRANSFORM_SCHEME, OBJ_FILTER
from logger_logic import logg
import unittest


class ConditionBase(ABC):
    name_resolver = {"OrCond": "or", "AndCond": "and", "NotCond": "not",
                     "IsUserCond": "is_user", "IsGroupCond": "is_group", "FieldsOpCond": "fields_op",
                     "RegexpCond": "regexp"}

    def __init__(self, condition_data: dict):
        self.condition_data = condition_data
        self.validator(condition_data)

    def validator(self, condition_data: dict):
        pass

    def get_my_name(self) -> str:
        return self.name_resolver[self.__class__.__name__]

    def field_error(self, field: str):
        raise KeyError(
            f"Error in condition {self.get_my_name()}. The mandatory '{field}' field was not found in the condition:"
            f"\n{self.condition_data}")

    def type_error(self, field: str, variants: set[str]):
        raise TypeError(
            f"Error in condition {self.get_my_name()}. {field} must be ({variants}) in the condition:"
            f"\n{self.condition_data}")

    def general_error(self, error: Type[Exception], msg: str):
        raise error(f"Error in condition {self.get_my_name()}. {msg}:\n{self.condition_data}")


class OrCond(ConditionBase):
    def validator(self, condition_data: dict):
        if "conditions" in condition_data:
            if not condition_data["conditions"]:
                self.general_error(ValueError, "Conditions cannot be empty")
            for condition in condition_data["conditions"]:
                condition_validator(condition)
        else:
            self.field_error("conditions")


class AndCond(ConditionBase):
    def validator(self, condition_data: dict):
        if "conditions" in condition_data:
            if not condition_data["conditions"]:
                self.general_error(ValueError, "Conditions cannot be empty")
            for condition in condition_data["conditions"]:
                condition_validator(condition)
        else:
            self.field_error("conditions")


class NotCond(ConditionBase):
    def validator(self, condition_data: dict):
        if "condition" in condition_data:
            condition_validator(condition_data["condition"])
        else:
            self.field_error("condition")


class IsUserCond(ConditionBase):
    pass


class IsGroupCond(ConditionBase):
    pass


class FieldsOpCond(ConditionBase):
    condition_data: dict

    def validator(self, condition_data: dict):
        if "op" in condition_data:
            if condition_data["op"] in {"<", ">", "<=", ">=", "==", "!=", "in"}:
                pass
            else:
                self.type_error("op", {"<", ">", "<=", ">=", "==", "!=", "in"})
        else:
            self.field_error("op")
        if "l_v" in condition_data:
            l_v = condition_data["l_v"]
            self.value_validate(l_v)
        else:
            self.field_error("l_v")
        if "r_v" in condition_data:
            r_v = condition_data["r_v"]
            self.value_validate(r_v)
        else:
            self.field_error("r_v")

    def value_validate(self, value_data: dict[str, str]):
        if "source" in value_data:
            if value_data["source"] in {"object", "computer"}:
                if "field" in value_data:
                    if value_data["source"] == "object":
                        field = value_data["field"]
                        if (field in TRANSFORM_SCHEME["user"].values()
                                or field in TRANSFORM_SCHEME["group"].values()):
                            pass
                        else:
                            self.general_error(ValueError, f"Field '{field}' not found in the schema")
                else:
                    self.field_error("field")
            elif value_data["source"] == "const":
                if "value" in value_data:
                    pass
                else:
                    self.field_error("value")
            else:
                self.type_error("source", {"const", "object", "computer"})
        else:
            self.field_error("source")


class RegexpCond(ConditionBase):
    def validator(self, condition_data: dict):
        if "value" in condition_data:
            pass
        else:
            self.field_error("value")
        if "field" in condition_data:
            pass
        else:
            self.field_error("field")


def condition_validator(condition: dict):
    if "cond_type" in condition:
        condition_type: str = condition["cond_type"]
        resolver_dict = {"or": OrCond, "and": AndCond, "not": NotCond, "is_user": IsUserCond, "is_group": IsGroupCond,
                         "fields_op": FieldsOpCond, "regexp": RegexpCond}
        if condition_type in resolver_dict:
            resolver_dict[condition_type](condition)
        else:
            raise TypeError(f"unknown condition {condition_type}")
    else:
        raise KeyError(f"condition type not defined in:\n{condition}")


@logg()
def validate_obj_filter():
    condition_validator(OBJ_FILTER)


class ValidatorsTests(unittest.TestCase):
    def test_or_and_value_error(self):
        for cond_type in ("or", "and"):
            try:
                conditions = {"cond_type": cond_type, "conditions": []}
                condition_validator(conditions)
                self.assertTrue(False)
            except ValueError:
                self.assertTrue(True)

    def test_or_and(self):
        for cond_type in ("or", "and"):
            conditions = {"cond_type": cond_type, "conditions": [{"cond_type": "is_user"}]}
            condition_validator(conditions)
            self.assertTrue(True)

    def test_or_and_rec(self):
        for cond_type in ("or", "and"):
            conditions = {"cond_type": cond_type,
                          "conditions": [{"cond_type": cond_type, "conditions": [{"cond_type": "is_user"}]}]}
            condition_validator(conditions)
            self.assertTrue(True)

    def test_not(self):
        conditions = {"cond_type": "not", "condition": {"cond_type": "is_user"}}
        condition_validator(conditions)
        self.assertTrue(True)

    def test_fields_op(self):
        TRANSFORM_SCHEME = {"user": {
            "Имя учетной записи пользователя": "name",
            "dn": "dn",
            "Link to department": "ltd"
        },
            "group": {
                "Имя группы": "name",
                "Link to department": "ltd"
            }
        }
        conditions = {"cond_type": "fields_op",
                      "l_v": {"source": "const", "value": 1},
                      "r_v": {"source": "object", "field": "ltd"},
                      "op": "=="}
        condition_validator(conditions)
        self.assertTrue(True)

    def test_regexp(self):
        conditions = {"cond_type": "regexp",
                      "value": "test",
                      "field": ""}
        condition_validator(conditions)
        self.assertTrue(True)
