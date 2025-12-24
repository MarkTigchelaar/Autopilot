import Tokenization.symbols as symbols
from Parsing.utils import (
    is_eof_type,
    is_eof_type,
    is_valid_index_token
)
from ErrorHandling.parsing_error_messages import *
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from ASTComponents.InternalComponents.for_statement import ForStatement


def parse_for(driver):
    for_token = driver.next_token()
    enforce_for(for_token)
    peek_token = driver.peek_token()
    for_stmt = ForStatement()
    for_stmt.add_descriptor_token(for_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.LET:
        return assign_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.VAR:
        return assign_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return index_or_key_var_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def assign_step(driver, for_stmt):
    assign_token = driver.next_token()
    for_stmt.add_assignment_type(assign_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return unwrapped_option_main_var_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def unwrapped_option_main_var_step(driver, for_stmt):
    unwrapped_option_var_token = driver.next_token()
    for_stmt.add_variable_name(unwrapped_option_var_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IN:
        return in_option_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.COMMA:
        return comma_option_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def comma_option_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return unwrapped_option_second_var_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def unwrapped_option_second_var_step(driver, for_stmt):
    unwrapped_option_var_token = driver.next_token()
    for_stmt.add_second_variable_name(unwrapped_option_var_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IN:
        return in_option_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def in_option_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return option_collection_var_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def option_collection_var_step(driver, for_stmt):
    option_collection_var_token = driver.next_token()
    for_stmt.add_option_collection(option_collection_var_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.AS:
        return as_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.DO:
        return do_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def index_or_key_var_step(driver, for_stmt):
    index_or_key_name_token = driver.next_token()
    for_stmt.add_index_or_key_name(index_or_key_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.COMMA:
        return key_value_comma_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.IN:
        return in_range_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def key_value_comma_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return key_value_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def key_value_step(driver, for_stmt):
    key_value_name_token = driver.next_token()
    for_stmt.add_map_value_name(key_value_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IN:
        return in_range_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def in_range_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return collection_or_index_start_step(driver, for_stmt)
    elif is_valid_index_token(peek_token):
        return index_start_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def collection_or_index_start_step(driver, for_stmt):
    collection_or_index_start_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.RANGE:
        for_stmt.add_index_start_name(collection_or_index_start_token)
        return range_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.AS:
        for_stmt.add_collection_name(collection_or_index_start_token)
        return as_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.DO:
        for_stmt.add_collection_name(collection_or_index_start_token)
        return do_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def index_start_step(driver, for_stmt):
    index_start_token = driver.next_token()
    for_stmt.add_index_start_name(index_start_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.RANGE:
        return range_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def range_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return index_stop_step(driver, for_stmt)
    elif is_valid_index_token(peek_token):
        return index_stop_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def index_stop_step(driver, for_stmt):
    index_stop_token = driver.next_token()
    for_stmt.add_index_stop_name(index_stop_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.COMMA:
        return iteration_comma_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.AS:
        return as_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.DO:
        return do_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def iteration_comma_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return iteration_step_length_step(driver, for_stmt)
    elif is_valid_index_token(peek_token):
        return iteration_step_length_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def iteration_step_length_step(driver, for_stmt):
    iteration_step_token = driver.next_token()
    for_stmt.add_iteration_step_size(iteration_step_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.AS:
        return as_step(driver, for_stmt)
    elif peek_token.internal_type == symbols.DO:
        return do_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def as_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return loop_name_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def loop_name_step(driver, for_stmt):
    loop_name_token = driver.next_token()
    for_stmt.add_loop_name(loop_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.DO:
        return do_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, for_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    return statements_step(driver, for_stmt)


def statements_step(driver, for_stmt):
    if driver.is_unit_testing():
        stmts = []
    else:
        stmts = parse_statements(driver, True)
    if driver.has_errors():
        return None
    for_stmt.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.ENDSCOPE:
        return end_step(driver, for_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, for_stmt):
    driver.discard_token()
    return for_stmt


def enforce_for(for_token):
    if for_token.internal_type != symbols.FOR:
        raise Exception(
            "INTERNAL ERROR: expected for statement, got " + for_token.literal
        )
