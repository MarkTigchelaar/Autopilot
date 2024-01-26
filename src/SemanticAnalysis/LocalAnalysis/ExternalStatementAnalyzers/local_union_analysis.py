from ErrorHandling.semantic_error_messages import *
from symbols import IDENTIFIER

def analyze_union(analyzer, union_ast_node):
    fields = union_ast_node.items
    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            check_fields_for_duplicate_names(analyzer, fields[i], fields[j])
            check_fields_for_duplicate_types(analyzer, fields[i], fields[j])
        check_field_if_name_matches_union(analyzer, fields[i], union_ast_node.name_token)


def check_fields_for_duplicate_names(analyzer, field_one, field_two):
    if field_one.item_name_token.literal == field_two.item_name_token.literal:
        analyzer.add_error(field_two.item_name_token, DUPLICATE_UNION_FIELD_NAME)


def check_fields_for_duplicate_types(analyzer, field_one, field_two):
    if field_one.type_token.type_symbol == field_two.type_token.type_symbol:
        if field_one.type_token.type_symbol != IDENTIFIER:
            analyzer.add_error(field_two.type_token, DUPLICATE_UNION_FIELD_TYPE)
        elif field_one.type_token.literal == field_two.type_token.literal:
            analyzer.add_error(field_two.item_name_token, DUPLICATE_UNION_FIELD_TYPE)


def check_field_if_name_matches_union(analyzer, field_one, union_name):
    if field_one.item_name_token.literal == union_name.literal:
        analyzer.add_error(field_one.item_name_token, UNION_AND_FIELD_NAME_COLLISION)
