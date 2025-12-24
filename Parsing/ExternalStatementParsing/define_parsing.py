import Tokenization.symbols as symbols
from Parsing.utils import (
    is_eof_type,
    is_eof_type,
    is_primitive_type,
    is_key_value_collection_type,
    is_list_collection_type,
    is_hash_collection_type,
    is_queue_collection_type,
)
from ErrorHandling.parsing_error_messages import *

from ASTComponents.ExternalComponents.define_statements import (
    KeyValueType,
    HashType,
    ListType,
    QueueType,
    StackType,
    OptionType,
    ResultType,
    FunctionType,
)


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
        return key_value_collection_step(driver)
    elif is_list_collection_type(peek_token):
        return list_collection_type_step(driver)
    elif is_hash_collection_type(peek_token):
        return hash_collection_type_step(driver)
    elif peek_token.internal_type == symbols.STACK:
        return stack_collection_step_type(driver)
    elif is_queue_collection_type(peek_token):
        return queue_collection_type_step(driver)

    elif peek_token.internal_type == symbols.OPTION:
        return option_type_step(driver)
    elif peek_token.internal_type == symbols.RESULT:
        return result_type_step(driver)
    elif peek_token.internal_type == symbols.FUN:
        return function_type_step(driver)
    elif peek_token.internal_type == symbols.IDENTIFIER:
        driver.add_error(peek_token, DEFINE_RENAME_ERROR)
        return None
    else:
        driver.add_error(peek_token, INVALID_DEFINITION)
        return None


def key_value_collection_step(driver):
    type_token = driver.next_token()
    hash_type = KeyValueType()
    hash_type.add_type_variant_token(type_token)
    #hash_type.add_new_name_token(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.LEFT_PAREN:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.COLON:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
        return right_paren_step(driver, hash_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def list_collection_type_step(driver):
    linear_type = ListType()
    return linear_collection_type_step(driver, linear_type)


def hash_collection_type_step(driver):
    linear_type = HashType()
    return linear_collection_type_step(driver, linear_type)


def stack_collection_step_type(driver):
    linear_type = StackType()
    return linear_collection_type_step(driver, linear_type)


def queue_collection_type_step(driver):
    linear_type = QueueType()
    return linear_collection_type_step(driver, linear_type)


def linear_collection_type_step(driver, linear_type):
    type_token = driver.next_token()
    linear_type.add_type_variant_token(type_token)
    #linear_type.add_new_name_token(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.LEFT_PAREN:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
        return right_paren_step(driver, linear_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def option_type_step(driver):
    option = OptionType()
    return special_union_type_step(driver, option, True)


def result_type_step(driver):
    result = ResultType()
    return special_union_type_step(driver, result)


def special_union_type_step(driver, failable_type, is_option=False):
    type_token = driver.next_token()
    failable_type.add_type_variant_token(type_token)
    #failable_type.add_new_name_token(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.LEFT_PAREN:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
        if is_option:
            return right_paren_step(driver, failable_type)
        else:
            driver.add_error(peek_token, UNEXPECTED_TOKEN)
            return None
    elif peek_token.internal_type == symbols.COMMA:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return failable_type_alternate_step(driver, failable_type)
    elif is_primitive_type(peek_token):
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
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
        return right_paren_step(driver, failable_type)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_type_step(driver):
    fn_token = driver.next_token()
    peek_token = driver.peek_token()
    function_type = FunctionType()
    function_type.add_type_variant_token(fn_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.LEFT_PAREN:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return function_arg_type_value_step(driver, function_type)
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
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
    elif peek_token.internal_type == symbols.COMMA:
        return function_comma_step(driver, function_type)
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return function_return_type_value_step(driver, function_type)
    elif peek_token.internal_type == symbols.AS:
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
    elif peek_token.internal_type == symbols.AS:
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
    elif peek_token.internal_type == symbols.AS:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return new_name_step(driver, sub_type)
    else:
        driver.add_error(peek_token, INVALID_DEFINITION)
        return None


def new_name_step(driver, define_stmt):
    definition_token = driver.next_token()
    define_stmt.add_new_name_token(definition_token)
    return define_stmt


def enforce_define(token):
    if token.internal_type != symbols.DEFINE:
        raise Exception("INTERNAL ERROR: expected define, got " + token.literal)
