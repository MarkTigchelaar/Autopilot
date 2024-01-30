import symbols
from keywords import is_eof_type, is_primitive_type, \
is_key_value_collection_type, is_linear_collection_type
from ErrorHandling.parsing_error_messages import *
from ASTComponents import ast_node_keys

def parse_define(driver):
    token = driver.next_token()
    enforce_define(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif is_key_value_collection_type(peek_token):
        return hash_collection_step(driver)
    elif is_linear_collection_type(peek_token):
        return linear_collection_type_step(driver)
    elif peek_token.type_symbol == symbols.OPTION:
        return special_union_type_step(driver, True)
    elif peek_token.type_symbol == symbols.RESULT:
        return special_union_type_step(driver)
    elif peek_token.type_symbol == symbols.FUN:
        return function_type_step(driver)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        driver.add_error(peek_token, DEFINE_RENAME_ERROR)
        return None
    else:
        driver.add_error(peek_token, INVALID_DEFINITION)
        return None


def hash_collection_step(driver):
    type_token = driver.next_token()
    hash_type = driver.make_node(ast_node_keys.KV_DEFINE)
    hash_type.add_type_token(type_token)
    hash_type.add_descriptor_token(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LEFT_PAREN:
        return hash_left_paren_step(driver, hash_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def hash_left_paren_step(driver, hash_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return hash_key_step(driver, hash_type)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return hash_key_step(driver, hash_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def hash_key_step(driver, hash_type):
    key_token = driver.next_token()
    hash_type.add_key_token(key_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COLON:
        return hash_colon_step(driver, hash_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def hash_colon_step(driver, hash_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return hash_value_step(driver, hash_type)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return hash_value_step(driver, hash_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def hash_value_step(driver, hash_type):
    value_token = driver.next_token()
    hash_type.add_value_token(value_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return right_paren_step(driver, hash_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def linear_collection_type_step(driver):
    type_token = driver.next_token()
    linear_type = driver.make_node(ast_node_keys.LINEAR_DEFINE)
    linear_type.add_type_token(type_token)
    linear_type.add_descriptor_token(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LEFT_PAREN:
        return linear_left_paren_step(driver, linear_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def linear_left_paren_step(driver, linear_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return linear_value_step(driver, linear_type)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return linear_value_step(driver, linear_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def linear_value_step(driver, linear_type):
    value_token = driver.next_token()
    linear_type.add_value_token(value_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return right_paren_step(driver, linear_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def special_union_type_step(driver, is_option = False):
    type_token = driver.next_token()
    failable_type = driver.make_node(ast_node_keys.FAIL_DEFINE)
    failable_type.add_type_token(type_token)
    failable_type.add_descriptor_token(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LEFT_PAREN:
        return left_paren_failable_type_step(driver, failable_type, is_option)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def left_paren_failable_type_step(driver, failable_type, is_option):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return failable_type_value_step(driver, failable_type, is_option)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return failable_type_value_step(driver, failable_type, is_option)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def failable_type_value_step(driver, failable_type, is_option):
    value_token = driver.next_token()
    failable_type.add_value_token(value_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        if is_option:
            return right_paren_step(driver, failable_type)
        else:
            driver.add_error(peek_token, UNEXPECTED_TOKEN)
            return None
    elif peek_token.type_symbol == symbols.COMMA:
        return failable_type_comma_step(driver, failable_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def failable_type_comma_step(driver, failable_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return failable_type_alternate_step(driver, failable_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def failable_type_alternate_step(driver, failable_type):
    alternate_value_token = driver.next_token()
    failable_type.add_alternate_token(alternate_value_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return right_paren_step(driver, failable_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_type_step(driver):
    fn_token = driver.next_token()
    peek_token = driver.peek_token()
    function_type = driver.make_node(ast_node_keys.FN_SIG_DEFINE)
    function_type.add_descriptor_token(fn_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LEFT_PAREN:
        return function_left_paren_step(driver, function_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_left_paren_step(driver, function_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return function_arg_type_value_step(driver, function_type)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return function_arg_type_value_step(driver, function_type)
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return function_right_paren_step(driver, function_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_arg_type_value_step(driver, function_type):
    arg_type_token = driver.next_token()
    function_type.add_argument(arg_type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        return function_comma_step(driver, function_type)
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return function_right_paren_step(driver, function_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_comma_step(driver, function_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return function_arg_type_value_step(driver, function_type)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return function_arg_type_value_step(driver, function_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_right_paren_step(driver, function_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token):
        return function_return_type_value_step(driver, function_type)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return function_return_type_value_step(driver, function_type)
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, function_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_return_type_value_step(driver, function_type):
    return_type_token = driver.next_token()
    function_type.add_return_type(return_type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, function_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def right_paren_step(driver, sub_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, sub_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def as_step(driver, sub_type):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return new_name_step(driver, sub_type)
    else:
        driver.add_error(peek_token, INVALID_DEFINITION)
        return None


def new_name_step(driver, sub_type):
    definition_token = driver.next_token()
    define_stmt = driver.make_node(ast_node_keys.DEFINE)
    define_stmt.add_subtype(sub_type)
    define_stmt.add_definition(definition_token)
    define_stmt.add_descriptor_token(definition_token)
    return define_stmt


def enforce_define(token):
    if token.type_symbol != symbols.DEFINE:
        raise Exception("INTERNAL ERROR: expected define, got " + token.literal)
