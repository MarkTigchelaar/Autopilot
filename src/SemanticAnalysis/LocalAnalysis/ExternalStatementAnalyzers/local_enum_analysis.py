import symbols
from ErrorHandling.semantic_error_messages import *
from keywords import is_primitive_type, is_boolean_literal


def analyze_enum(analyzer, enum_ast_node):
    check_if_enum_is_allowed_enum_type(analyzer, enum_ast_node)

    fields = enum_ast_node.item_list
    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            check_fields_for_duplicate_names(analyzer, fields[i], fields[j])
            check_fields_for_duplicate_values(analyzer, fields[i], fields[j])
            if enum_ast_node.general_type is None:
                check_fields_for_mismatched_types(analyzer, fields[i], fields[j])
        check_field_if_type_matches_enum(analyzer, fields[i], enum_ast_node)
        check_field_if_name_matches_enum(analyzer, fields[i], enum_ast_node)
        check_if_field_is_allowed_enum_type(analyzer, fields[i])


def check_if_enum_is_allowed_enum_type(analyzer, enum_ast_node):
    if enum_ast_node.general_type is None:
        return
    if not is_primitive_type(enum_ast_node.general_type):
        analyzer.add_error(enum_ast_node.general_type, ENUM_HAS_UDT)


def check_fields_for_duplicate_names(analyzer, field_one, field_two):
    if field_one.item_name_token.literal == field_two.item_name_token.literal:
        analyzer.add_error(field_two.item_name_token, ENUM_DUP_FIELD_NAME)


def check_fields_for_duplicate_values(analyzer, field_one, field_two):
    type1 = field_one.default_value_token
    type2 = field_two.default_value_token
    if None in (type1, type2):
        return
    if "null" in (type1.literal, type2.literal):
        return
    if type1.literal == type2.literal:
        analyzer.add_error(field_two.item_name_token, ENUM_DUP_VALUE)


def check_fields_for_mismatched_types(analyzer, field_one, field_two):
    type1 = field_one.default_value_token
    type2 = field_two.default_value_token
    if None in (type1, type2):
        return
    if "NULL" in (type1.type_symbol, type2.type_symbol):
        return
    if (type1.literal != type2.literal) and (not_a_bool(type1) and not_a_bool(type2)):
        if type1.type_symbol != type2.type_symbol:
            analyzer.add_error(field_two.item_name_token, ENUM_MISMATCHED_TYPE)


def check_field_if_type_matches_enum(analyzer, field_one, enum_ast_node):
    if enum_ast_node.general_type is None:
        return
    type1 = field_one.default_value_token
    if type1 is None:
        return
    if type1.type_symbol in ("NULL", symbols.IDENTIFIER):
        return
    if is_a_bool(type1) and is_a_bool(enum_ast_node.general_type):
        return
    if type1.type_symbol != enum_ast_node.general_type.type_symbol:
        analyzer.add_error(type1, ENUM_AND_FIELD_TYPE_MISMATCH)


def check_field_if_name_matches_enum(analyzer, field_one, enum_ast_node):
    name_token = field_one.item_name_token
    if name_token is None:
        return
    if name_token.literal == enum_ast_node.name.literal:
        analyzer.add_error(name_token, ENUM_AND_FIELD_NAME_COLLISION)


def check_if_field_is_allowed_enum_type(analyzer, field_one):
    type1 = field_one.default_value_token
    if type1 is None:
        return
    if not (is_primitive_type(type1) or is_boolean_literal(type1)):
        analyzer.add_error(field_one.item_name_token, ENUM_VALUE_IS_UDT)


def is_a_bool(type_token):
    return not not_a_bool(type_token)


def not_a_bool(type_token):
    symbol = type_token.type_symbol
    if symbol != symbols.TRUE and symbol != symbols.FALSE and symbol != symbols.BOOL:
        return True
    return False
