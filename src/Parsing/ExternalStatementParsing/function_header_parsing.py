import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ASTComponents import ast_node_keys

def parse_function_header(driver, is_function_def = True):
    function_token = driver.next_token()
    enforce_function(function_token)
    peek_token = driver.peek_token()
    fn_header_stmt = driver.make_node(ast_node_keys.FN_HEADER)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return function_name_step(driver, fn_header_stmt, is_function_def)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_name_step(driver, fn_header_stmt, is_function_def):
    name_token = driver.next_token()
    fn_header_stmt.add_name(name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LEFT_PAREN:
        return left_paren_step(driver, fn_header_stmt, is_function_def)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def left_paren_step(driver, fn_header_stmt, is_function_def):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return arg_name_step(driver, fn_header_stmt, is_function_def)
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return right_paren_step(driver, fn_header_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def arg_name_step(driver, fn_header_stmt, is_function_def):
    fn_arg = driver.make_node(ast_node_keys.FN_ARG_DEFINE)
    arg_name_token = driver.next_token()
    fn_arg.add_name(arg_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, fn_header_stmt, fn_arg, is_function_def)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def as_step(driver, fn_header_stmt, fn_arg, is_function_def):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return arg_type_step(driver, fn_header_stmt, fn_arg, is_function_def)
    elif is_primitive_type(peek_token, True):
        return arg_type_step(driver, fn_header_stmt, fn_arg, is_function_def)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def arg_type_step(driver, fn_header_stmt, fn_arg, is_function_def):
    arg_type_token = driver.next_token()
    fn_arg.add_type(arg_type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        fn_header_stmt.add_arg(fn_arg)
        return arg_comma_step(driver, fn_header_stmt, is_function_def)
    elif peek_token.type_symbol == symbols.EQUAL:
        if is_function_def:
            return assign_step(driver, fn_header_stmt, fn_arg, is_function_def)
        else:
            driver.add_error(peek_token, UNEXPECTED_TOKEN)
            return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        fn_header_stmt.add_arg(fn_arg)
        return right_paren_step(driver, fn_header_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def arg_comma_step(driver, fn_header_stmt, is_function_def):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return arg_name_step(driver, fn_header_stmt, is_function_def)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def assign_step(driver, fn_header_stmt, fn_arg, is_function_def):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_literal(peek_token):
        return default_value_step(driver, fn_header_stmt, fn_arg, is_function_def)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def default_value_step(driver, fn_header_stmt, fn_arg, is_function_def):
    default_value_token = driver.next_token()
    fn_arg.add_default_value(default_value_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        fn_header_stmt.add_arg(fn_arg)
        return arg_comma_step(driver, fn_header_stmt, is_function_def)
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        fn_header_stmt.add_arg(fn_arg)
        return right_paren_step(driver, fn_header_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def right_paren_step(driver, fn_header_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return return_type_step(driver, fn_header_stmt)
    elif is_primitive_type(peek_token, True):
        return return_type_step(driver, fn_header_stmt)
    else:
        return fn_header_stmt


def return_type_step(driver, fn_header_stmt):
    return_type_token = driver.next_token()
    fn_header_stmt.add_return_type(return_type_token)
    return fn_header_stmt


def enforce_function(function_token):
    if function_token.type_symbol != symbols.FUN:
        raise Exception("INTERNAL ERROR: expected function statement, got " + function_token.literal)
