import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys

def parse_switch(driver):
    switch_token = driver.next_token()
    enforce_switch(switch_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    switch_stmt = test_expression_step(driver)
    if switch_stmt:
        switch_stmt.add_descriptor_token(switch_token)
    return switch_stmt


def test_expression_step(driver):
    test_exp = parse_expression(driver)
    if driver.has_errors():
        return None
    if test_exp is None:
        return None
    switch_stmt = driver.make_node(ast_node_keys.SWITCH_STMT)
    switch_stmt.add_test_expression(test_exp)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.CASE:
        return case_step(driver, switch_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def case_step(driver, switch_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    case_stmt = driver.make_node(ast_node_keys.CASE_STMT)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return case_value_step(driver, switch_stmt, case_stmt)
    elif is_primitive_literal(peek_token):
        return case_value_step(driver, switch_stmt, case_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def case_value_step(driver, switch_stmt, case_stmt):
    value_token = driver.next_token()
    case_stmt.add_value(value_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        return comma_step(driver, switch_stmt, case_stmt)
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, switch_stmt, case_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def comma_step(driver, switch_stmt, case_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return case_value_step(driver, switch_stmt, case_stmt)
    elif is_primitive_literal(peek_token):
        return case_value_step(driver, switch_stmt, case_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, switch_stmt, case_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    return statements_step(driver, switch_stmt, case_stmt)


def statements_step(driver, switch_stmt, case_stmt, is_default = False):
    stmts = parse_statements(driver)
    if driver.has_errors():
        return None
    if stmts is None:
        return None
    case_stmt.add_statements(stmts)
    if is_default:
        switch_stmt.add_default_case(case_stmt)
    else:
        switch_stmt.add_case(case_stmt)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DEFAULT:
        return default_step(driver, switch_stmt)
    elif peek_token.type_symbol == symbols.CASE:
        return case_step(driver, switch_stmt)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, switch_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def default_step(driver, switch_stmt):
    default_token = driver.next_token()
    if switch_stmt.has_default_case():
        driver.add_error(default_token, EXISTING_DEFAULT)
        return None
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    default_case = driver.make_node(ast_node_keys.CASE_STMT)
    return statements_step(driver, switch_stmt, default_case, True)


def end_step(driver, switch_stmt):
    driver.discard_token()
    return switch_stmt


def enforce_switch(switch_token):
    if switch_token.type_symbol != symbols.SWITCH:
        raise Exception("INTERNAL ERROR: expected switch statement, got " + switch_token.literal)
