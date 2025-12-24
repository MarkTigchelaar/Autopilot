import Tokenization.symbols as symbols
from ErrorHandling.semantic_error_messages import (
    DUPLICATE_ERROR_FIELD_NAME,
    ERROR_AND_FIELD_NAME_COLLISION,
    INVALID_FIELD_TYPE
)


def analyze_error(analyzer, ast_node):
    error_name = ast_node.name_token
    fields = ast_node.items

    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            check_fields_for_duplicate_names(analyzer, fields[i], fields[j])
        check_field_name_matches_error(analyzer, fields[i], error_name)
        check_field_is_identifier(analyzer, fields[i])


def check_fields_for_duplicate_names(analyzer, field_one, field_two):
    if field_one.literal == field_two.literal:
        analyzer.add_error(field_one, DUPLICATE_ERROR_FIELD_NAME)


def check_field_name_matches_error(analyzer, field_one, error_name):
    if field_one.literal == error_name.literal:
        analyzer.add_error(field_one, ERROR_AND_FIELD_NAME_COLLISION)


def check_field_is_identifier(analyzer, field_one):
    if field_one.internal_type != symbols.IDENTIFIER:
        analyzer.add_error(field_one, INVALID_FIELD_TYPE)
