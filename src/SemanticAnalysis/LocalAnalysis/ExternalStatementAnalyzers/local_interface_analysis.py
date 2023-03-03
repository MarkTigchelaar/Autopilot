from ErrorHandling.semantic_error_messages import *

def analyze_interface(analyzer, ast_node):
    interface_name = ast_node.name_token.literal
    fn_defs = ast_node.fn_headers
    for i in range(len(fn_defs)):
        for j in range(i + 1, len(fn_defs)):
            check_fns_for_duplicate_names(analyzer, fn_defs[i], fn_defs[j])
            check_other_args_for_fn_name(analyzer, fn_defs[i], fn_defs[j])
        check_fn_args_for_duplicate_names(analyzer, fn_defs[i])
        check_fn_for_interface_name(analyzer, interface_name, fn_defs[i])
        check_fn_args_for_interface_and_fn_name(analyzer, interface_name, fn_defs[i])


def check_fns_for_duplicate_names(analyzer, fn_def_one, fn_def_two):
    if fn_def_one.name_token.literal == fn_def_two.name_token.literal:
        analyzer.add_error(fn_def_two.name_token, FUNCTION_NAME_COLLISION)


def check_other_args_for_fn_name(analyzer, fn_def_one, fn_def_two):
    function_args = fn_def_two.arguments
    for i in range(len(function_args)):
        if function_args[i].arg_name_token.literal == fn_def_one.name_token.literal:
            analyzer.add_error(function_args[i].arg_name_token, ARGUMENT_AND_PREV_FN_NAME_COLLISION)


def check_fn_args_for_duplicate_names(analyzer, fn_def_one):
    function_args = fn_def_one.arguments
    for i in range(len(function_args)):
        first_arg_name = function_args[i].arg_name_token.literal
        for j in range(i + 1, len(function_args)):
            secondary_arg_name = function_args[j].arg_name_token.literal
            if first_arg_name == secondary_arg_name:
                analyzer.add_error(function_args[j].arg_name_token, ARGUMENT_NAME_COLLISION)


def check_fn_for_interface_name(analyzer, interface_name, fn_def_one):
    fn_name = fn_def_one.name_token.literal
    if fn_name == interface_name:
        analyzer.add_error(fn_def_one.name_token, FN_AND_INTERFACE_NAME_COLLISION)


def check_fn_args_for_interface_and_fn_name(analyzer, interface_name, fn_def_one):
    fn_name = fn_def_one.name_token.literal
    function_args = fn_def_one.arguments
    for i in range(len(function_args)):
        arg_name = function_args[i].arg_name_token.literal
        if arg_name == fn_name:
            analyzer.add_error(function_args[i].arg_name_token, ARGUMENT_AND_FN_NAME_COLLISION)
        if arg_name == interface_name:
            analyzer.add_error(function_args[i].arg_name_token, ARGUMENT_AND_INTERFACE_NAME_COLLISION)
