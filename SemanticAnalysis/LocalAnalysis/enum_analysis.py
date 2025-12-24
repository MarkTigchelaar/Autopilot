import Tokenization.symbols as symbols
from Tokenization.token import Token
from ErrorHandling.semantic_error_messages import (
    BOOL_ENUM_TOO_MANY_FIELDS,
    CHAR_ENUM_TOO_MANY_FIELDS,
    ENUM_HAS_UDT,
    ENUM_DUP_VALUE,
    ENUM_DUP_FIELD_NAME,
    ENUM_MISMATCHED_TYPE,
    ENUM_AND_FIELD_TYPE_MISMATCH,
    ENUM_AND_FIELD_NAME_COLLISION,
    ENUM_VALUE_IS_UDT,
    ENUM_HAS_NO_TYPE,
)
from Parsing.utils import is_primitive_type, is_boolean_literal


def analyze_enum(error_manager, enum_ast_node):
    check_if_enum_is_allowed_enum_type(error_manager, enum_ast_node)

    fields = enum_ast_node.item_list
    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            check_fields_for_duplicate_names(error_manager, fields[i], fields[j])
            check_fields_for_duplicate_values(error_manager, fields[i], fields[j])
            if enum_ast_node.general_type is None:
                check_fields_for_mismatched_types(error_manager, fields[i], fields[j])
        check_field_if_type_matches_enum(error_manager, fields[i], enum_ast_node)
        check_field_if_name_matches_enum(error_manager, fields[i], enum_ast_node)
        check_if_field_is_allowed_enum_type(error_manager, fields[i])

    if enum_ast_node.general_type is None:
        find_and_assign_general_type(error_manager, enum_ast_node)
    check_if_bool_enum_has_more_than_two_fields(error_manager, enum_ast_node)
    check_if_char_enum_has_more_than_256_fields(error_manager, enum_ast_node)
    if is_primitive_type(enum_ast_node.general_type):
        assign_default_values(enum_ast_node)


def check_if_bool_enum_has_more_than_two_fields(error_manager, enum_ast_node):
    if enum_ast_node.general_type is None:
        return
    if enum_ast_node.general_type.internal_type == symbols.BOOL:
        if len(enum_ast_node.item_list) > 2:
            error_manager.add_error(
                enum_ast_node.item_list[2].item_name_token, BOOL_ENUM_TOO_MANY_FIELDS
            )
        elif len(enum_ast_node.item_list) < 1:
            raise Exception("Enums cannot be empty")


def check_if_char_enum_has_more_than_256_fields(error_manager, enum_ast_node):
    if enum_ast_node.general_type is None:
        return
    if enum_ast_node.general_type.internal_type == symbols.CHAR:
        if len(enum_ast_node.item_list) > 256:
            error_manager.add_error(
                enum_ast_node.item_list[255].item_name_token, CHAR_ENUM_TOO_MANY_FIELDS
            )


def check_if_enum_is_allowed_enum_type(error_manager, enum_ast_node):
    if enum_ast_node.general_type is None:
        return
    if not is_primitive_type(enum_ast_node.general_type):
        error_manager.add_error(enum_ast_node.general_type, ENUM_HAS_UDT)


def find_and_assign_general_type(error_manager, enum_ast_node):
    fields = enum_ast_node.get_items()
    default_value = None
    for field in fields:
        default_value = field.get_value()
        if default_value:
            break
    if default_value is None:
        error_manager.add_error(enum_ast_node.get_name(), ENUM_HAS_NO_TYPE)
        return
    general_type_token = Token()
    general_type_token.internal_type = default_value.internal_type
    enum_ast_node.add_general_type(general_type_token)


def check_fields_for_duplicate_names(error_manager, field_one, field_two):
    if field_one.item_name_token.literal == field_two.item_name_token.literal:
        error_manager.add_error(field_two.item_name_token, ENUM_DUP_FIELD_NAME)


def check_fields_for_duplicate_values(error_manager, field_one, field_two):
    type1 = field_one.default_value_token
    type2 = field_two.default_value_token
    if None in (type1, type2):
        return
    if "null" in (type1.literal, type2.literal):
        return
    if type1.literal == type2.literal:
        error_manager.add_error(field_two.item_name_token, ENUM_DUP_VALUE)


def check_fields_for_mismatched_types(error_manager, field_one, field_two):
    type1 = field_one.default_value_token
    type2 = field_two.default_value_token
    if None in (type1, type2):
        return
    if "NULL" in (type1.internal_type, type2.internal_type):
        return
    if (type1.literal != type2.literal) and (not_a_bool(type1) and not_a_bool(type2)):
        if type1.internal_type != type2.internal_type:
            error_manager.add_error(field_two.item_name_token, ENUM_MISMATCHED_TYPE)


def check_field_if_type_matches_enum(error_manager, field_one, enum_ast_node):
    if enum_ast_node.general_type is None:
        return
    type1 = field_one.default_value_token
    if type1 is None:
        return
    if type1.internal_type in ("NULL", symbols.IDENTIFIER):
        return
    if is_a_bool(type1) and is_a_bool(enum_ast_node.general_type):
        return
    if type1.internal_type != enum_ast_node.general_type.internal_type:
        error_manager.add_error(type1, ENUM_AND_FIELD_TYPE_MISMATCH)


def check_field_if_name_matches_enum(error_manager, field_one, enum_ast_node):
    name_token = field_one.item_name_token
    if name_token is None:
        return
    if name_token.literal == enum_ast_node.get_name().literal:
        error_manager.add_error(name_token, ENUM_AND_FIELD_NAME_COLLISION)


def check_if_field_is_allowed_enum_type(error_manager, field_one):
    type1 = field_one.default_value_token
    if type1 is None:
        return
    if not (is_primitive_type(type1) or is_boolean_literal(type1)):
        error_manager.add_error(field_one.item_name_token, ENUM_VALUE_IS_UDT)


def is_a_bool(type_token):
    return not not_a_bool(type_token)


def not_a_bool(type_token):
    symbol = type_token.internal_type
    if symbol != symbols.TRUE and symbol != symbols.FALSE and symbol != symbols.BOOL:
        return True
    return False


def assign_default_values(enum_ast_node):
    fields = enum_ast_node.get_items()
    current_default_value_tokens = list()
    for field in fields:
        default_value = field.get_value()
        if default_value:
            current_default_value_tokens.append(default_value.literal)
    primitive_sequence = None
    match enum_ast_node.get_general_type().internal_type:
        case symbols.INT:
            primitive_sequence = IntSequence(current_default_value_tokens)
        case symbols.LONG:
            primitive_sequence = LongSequence(current_default_value_tokens)
        case symbols.FLOAT:
            primitive_sequence = FloatSequence(current_default_value_tokens)
        case symbols.DOUBLE:
            primitive_sequence = DoubleSequence(current_default_value_tokens)
        case symbols.CHAR:
            primitive_sequence = CharSequence(current_default_value_tokens)
        case symbols.STRING:
            primitive_sequence = StringSequence(current_default_value_tokens)
        case symbols.BOOL:
            primitive_sequence = BoolSequence(current_default_value_tokens)
    if primitive_sequence is None:
        raise Exception("Primitive sequencer is None")

    for field in fields:
        default_value = field.get_value()
        if default_value:
            continue
        default_value_token = primitive_sequence.next()
        field.set_default_value(default_value_token)


class PrimitiveSequence:
    def __init__(self, default_values, start_value):
        self.existing_default_values = default_values
        self.start_value = start_value

    def next(self):
        self.inc()
        return self.start_value

    def inc(self):
        while self.start_value in self.existing_default_values:
            self.get_next_value()
        self.existing_default_values.append(self.start_value)


class IntSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, 0)

    def get_next_value(self):
        self.start_value += 1


class LongSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, 0)

    def get_next_value(self):
        self.start_value += 1


class FloatSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, 0.0)

    def get_next_value(self):
        self.start_value += 1.0


class DoubleSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, 0.0)

    def get_next_value(self):
        self.start_value += 1.0


class CharSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, chr(0))

    def get_next_value(self):
        # No safeguards, since check was done above
        self.start_value = chr(ord(self.start_value) + 1)


class StringSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, "a")

    def get_next_value(self):
        self.start_value = self.start_value + "a"


class BoolSequence(PrimitiveSequence):
    def __init__(self, default_values):
        super().__init__(default_values, "true")

    def get_next_value(self):
        # No safeguards, since check was done above
        if self.start_value == "true":
            self.start_value = "false"
        elif self.start_value == "false":
            self.start_value = "true"
        else:
            raise Exception("boolean value not valid")
