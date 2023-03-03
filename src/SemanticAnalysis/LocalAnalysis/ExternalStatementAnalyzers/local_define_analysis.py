import symbols
from ErrorHandling.semantic_error_messages import *
from keywords import is_key_value_collection_type, is_linear_collection_type

# Existance of types, and if valid types are being used
# for hashes (not enums, unions, functions and errors)
# are checked in global analysis
# Also checked are errors on both sides of results as well as other things
def analyze_define(analyzer, ast_node):
    # figure out code paths by using each types type_token
    type_token = get_type_token(ast_node)
    if is_key_value_collection_type(type_token):
        analyze_kv_type(analyzer, ast_node)
    elif is_linear_collection_type(type_token):
        analyze_linear_collection(analyzer, ast_node)
    elif type_token.type_symbol == symbols.OPTION:
        analyze_linear_collection(analyzer, ast_node)
    elif type_token.type_symbol == symbols.RESULT:
        analyze_result(analyzer, ast_node)
    elif type_token.type_symbol == symbols.FUN:
        analyze_function(analyzer, ast_node)
    else:
        raise Exception("INTERNAL ERROR: unknown type definition")


def get_type_token(ast_node):
    return ast_node.sub_type.type_token


def analyze_kv_type(analyzer, ast_node):
    sub_type = ast_node.sub_type
    name = ast_node.new_type_name_token.literal
    if name == sub_type.key_token.literal:
        analyzer.add_error(sub_type.key_token, DEFINED_NAME_COLLISION_WITH_COMPONENT)
    if name == sub_type.value_token.literal:
        analyzer.add_error(sub_type.value_token, DEFINED_NAME_COLLISION_WITH_COMPONENT)


def analyze_linear_collection(analyzer, ast_node):
    sub_type = ast_node.sub_type
    name = ast_node.new_type_name_token.literal
    if name == sub_type.value_token.literal:
        analyzer.add_error(sub_type.value_token, DEFINED_NAME_COLLISION_WITH_COMPONENT)


def analyze_result(analyzer, ast_node):
    sub_type = ast_node.sub_type
    name = ast_node.new_type_name_token.literal
    if name == sub_type.value_token.literal:
        analyzer.add_error(sub_type.value_token, DEFINED_NAME_COLLISION_WITH_COMPONENT)
    if name == sub_type.error_token.literal:
        analyzer.add_error(sub_type.error_token, DEFINED_NAME_COLLISION_WITH_COMPONENT)


def analyze_function(analyzer, ast_node):
    sub_type = ast_node.sub_type
    name = ast_node.new_type_name_token.literal
    if sub_type.return_type_token and name == sub_type.return_type_token.literal:
        analyzer.add_error(sub_type.return_type_token, DEFINED_NAME_COLLISION_WITH_COMPONENT)
    for arg_type in sub_type.arg_type_list:
        if name == arg_type.literal:
            analyzer.add_error(arg_type, DEFINED_NAME_COLLISION_WITH_COMPONENT)
