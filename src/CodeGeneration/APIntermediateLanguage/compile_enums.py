from symbols import *


def compile_enums(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for enum in raw_module.enums:
        compiled_module.append(f"{str_spaces}DEFINE ENUM {enum.get_name().literal}")
        general_type = find_general_type(enum)
        compiled_module.append(f"{str_spaces}TYPE {general_type}")
        enum_items = process_enum_fields(enum, general_type)
        for enum_value in enum_items:
            compiled_module.append(
                f"{str_spaces}{str_spaces}FIELD {enum_value.item_name} {enum_value.default_value}"
            )
        compiled_module.append(f"{str_spaces}END ENUM {enum.get_name().literal}")


def find_general_type(enum):
    general_type = enum.get_general_type()
    if general_type is None:
        for item in enum.items:
            if item.default_value_token is not None:
                type_name = item.default_value_token.get_type()
                if type_name in (TRUE, FALSE):
                    return BOOL
                return type_name
        return INT
    type_name = general_type.get_type()
    if type_name in (TRUE, FALSE):
        return BOOL
    return type_name


def process_enum_fields(enum, general_type):
    _type = general_type
    if _type in (INT, LONG):
        return process_int_enum(enum)
    if _type == BOOL:
        return process_bool_enum(enum)
    if _type in (FLOAT, DOUBLE):
        return process_float_enum(enum)
    if _type == CHAR:
        return process_char_enum(enum)
    if _type == STRING:
        return process_string_enum(enum)

    raise ValueError(f"Invalid enum type: {_type}")


class EnumValue:
    def __init__(self, item_name, default_value):
        self.item_name = item_name
        self.default_value = default_value


def process_int_enum(enum):
    no_defaults = []
    with_defaults = []
    result = []
    for item in enum.items:
        if item.default_value_token is None:
            no_defaults.append(item)
        else:
            with_defaults.append(item)

    with_defaults.sort(key=lambda x: int(x.default_value_token.literal), reverse=True)
    max_default = int(with_defaults[0].default_value_token.literal)
    no_defaults.reverse()

    while len(with_defaults) > 0:
        item = with_defaults.pop()
        result.append(
            EnumValue(item.item_name_token.literal, item.default_value_token.literal)
        )
        default = int(item.default_value_token.literal)
        if len(with_defaults) == 0:
            break
        next_default = int(with_defaults[-1].default_value_token.literal)
        gap = next_default - default
        while len(no_defaults) > 0 and gap > 1:
            no_default = no_defaults.pop()
            result.append(EnumValue(no_default.item_name_token.literal, default + 1))
            gap -= 1
    while len(no_defaults) > 0:
        item = no_defaults.pop()
        result.append(EnumValue(item.item_name_token.literal, max_default + 1))
        max_default += 1

    return result


def process_bool_enum(enum):
    result = []
    if len(enum.items) != 2:
        raise ValueError("Bool enum must have exactly 2 fields")
    item_one = enum.items[0]
    item_two = enum.items[1]
    if item_one.default_value_token.literal == "true":
        result.append(EnumValue(item_one.item_name_token.literal, "true"))
        result.append(EnumValue(item_two.item_name_token.literal, "false"))
    else:
        result.append(EnumValue(item_one.item_name_token.literal, "false"))
        result.append(EnumValue(item_two.item_name_token.literal, "true"))
    return result


def process_float_enum(enum):
    result = []
    no_defaults = []
    with_defaults = []
    for item in enum.items:
        if item.default_value_token is None:
            no_defaults.append(item)
        else:
            with_defaults.append(item)
    with_defaults.sort(key=lambda x: float(x.default_value_token.literal), reverse=True)
    max_default = float(with_defaults[0].default_value_token.literal)
    no_defaults.reverse()
    while len(with_defaults) > 0:
        item = with_defaults.pop()
        result.append(
            EnumValue(item.item_name_token.literal, item.default_value_token.literal)
        )
        default = float(item.default_value_token.literal)
        if len(with_defaults) == 0:
            break
        next_default = float(with_defaults[-1].default_value_token.literal)
        gap = next_default - default
        while len(no_defaults) > 0 and gap > 1:
            no_default = no_defaults.pop()
            result.append(
                EnumValue(no_default.item_name_token.literal, str(default + 1))
            )
            gap -= 1
    while len(no_defaults) > 0:
        item = no_defaults.pop()
        result.append(EnumValue(item.item_name_token.literal, str(max_default + 1)))
        max_default += 1
    return result


def process_char_enum(enum):
    result = []
    no_defaults = []
    with_defaults = []
    for item in enum.items:
        if item.default_value_token is None:
            no_defaults.append(item)
        else:
            with_defaults.append(item)
    with_defaults.sort(
        key=lambda x: ord(x.default_value_token.literal[1]), reverse=True
    )
    max_default = ord(with_defaults[0].default_value_token.literal[1])
    no_defaults.reverse()
    while len(with_defaults) > 0:
        item = with_defaults.pop()
        result.append(
            EnumValue(item.item_name_token.literal, item.default_value_token.literal)
        )
        default = ord(item.default_value_token.literal[1])
        if len(with_defaults) == 0:
            break
        next_default = ord(with_defaults[-1].default_value_token.literal[1])
        gap = next_default - default
        while len(no_defaults) > 0 and gap > 1:
            no_default = no_defaults.pop()
            result.append(
                EnumValue(no_default.item_name_token.literal, "'" + chr(default + 1) + "'")
            )
            gap -= 1
    while len(no_defaults) > 0:
        item = no_defaults.pop()
        result.append(EnumValue(item.item_name_token.literal, "'" + chr(max_default + 1) + "'"))
        max_default += 1
    return result


def process_string_enum(enum):
    result = []
    no_defaults = []
    with_defaults = []
    for item in enum.items:
        if item.default_value_token is None:
            no_defaults.append(item)
        else:
            with_defaults.append(item)
    with_defaults.sort(key=lambda x: x.default_value_token.literal)
    no_defaults.reverse()
    for item in with_defaults:
        result.append(
            EnumValue(
                item.item_name_token.literal, item.default_value_token.literal[1:-1]
            )
        )
    default = 0
    for item in no_defaults:
        result.append(EnumValue(item.item_name_token.literal, "default" + str(default)))
        default += 1

    duplicates_found = True
    while duplicates_found:
        duplicates_found = False
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                if result[i].default_value == result[j].default_value:
                    result[j].default_value += "0"
                    duplicates_found = True

    result.sort(key=lambda x: x.default_value)
    for item in result:
        item.default_value = f'"{item.default_value}"'

    return result
