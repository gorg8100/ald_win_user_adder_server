from conditions_validator import validate_obj_filter
from transform_scheme_validator import validate_transform_scheme, schemes_injector
from commands_validation import validate_commands
from ipa_data_getter import write_data


def validate_all():
    validate_obj_filter()
    validate_transform_scheme()
    schemes_injector()
    validate_commands()


def main():
    validate_all()
    # write_data()
    return


if __name__ == '__main__':
    main()
