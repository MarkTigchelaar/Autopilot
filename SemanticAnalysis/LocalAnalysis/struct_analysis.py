from ErrorHandling.semantic_error_messages import *
from SemanticAnalysis.LocalAnalysis.function_analysis import (
    analyze_function,
)


def analyze_struct(analyzer, ast_node):
    analyze_fields(analyzer, ast_node)
    analyze_functions(analyzer, ast_node)
    analyze_interfaces(analyzer, ast_node)


def analyze_functions(analyzer, ast_node):
    check_for_duplicate_function_names(analyzer, ast_node)
    for function in ast_node.functions:
        if function.header.name_token.literal == ast_node.get_name().literal:
            analyzer.add_error(
                function.header.name_token,
                METHOD_NAME_COLLIDES_WITH_STRUCT_NAME,
                ast_node.get_name()
            )
        analyze_function(analyzer, function, ast_node.fields)


def check_for_duplicate_function_names(analyzer, ast_node):
    for i in range(len(ast_node.functions)):
        for j in range(i + 1, len(ast_node.functions)):
            fn_name_one = ast_node.functions[i].header.name_token.literal
            fn_name_two = ast_node.functions[j].header.name_token.literal
            if fn_name_one == fn_name_two:
                analyzer.add_error(
                    ast_node.functions[j].header.name_token, METHOD_NAME_COLLISION
                )


def analyze_fields(analyzer, ast_node):
    for i in range(len(ast_node.fields)):
        if ast_node.fields[i].field_name_token.literal == ast_node.get_name().literal:
            analyzer.add_error(
                ast_node.fields[i].field_name_token,
                STRUCT_FIELD_COLLIDES_WITH_STRUCT_NAME,
                ast_node.get_name()
            )
        for j in range(i + 1, len(ast_node.fields)):
            if (
                ast_node.fields[i].field_name_token.literal
                == ast_node.fields[j].field_name_token.literal
            ):
                analyzer.add_error(
                    ast_node.fields[j].field_name_token, STRUCT_FIELD_NAME_COLLISION
                )


def analyze_interfaces(analyzer, ast_node):
    for i in range(len(ast_node.interfaces)):
        if ast_node.interfaces[i].literal == ast_node.get_name().literal:
            analyzer.add_error(
                ast_node.interfaces[i],
                INTERFACE_NAME_COLLIDES_WITH_STRUCT_NAME,
                ast_node.get_name()
            )
        for j in range(i + 1, len(ast_node.interfaces)):
            if ast_node.interfaces[i].literal == ast_node.interfaces[j].literal:
                analyzer.add_error(
                    ast_node.interfaces[j], STRUCT_INTERFACE_NAME_COLLISION
                )
