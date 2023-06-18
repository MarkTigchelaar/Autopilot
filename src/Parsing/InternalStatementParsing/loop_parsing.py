import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys


def parse_loop(driver):
    loop_token = driver.next_token()
    enforce_loop(loop_token)
    loop_statement = driver.make_node(ast_node_keys.LOOP_STMT)
    loop_statement.add_descriptor_token(loop_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, loop_statement)
    else:
        return statements_step(driver, loop_statement)


def as_step(driver, loop_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return loop_name_step(driver, loop_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def loop_name_step(driver, loop_statement):
    loop_name_token = driver.next_token()
    loop_statement.add_loop_name(loop_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, loop_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, loop_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return statements_step(driver, loop_statement)


def statements_step(driver, loop_statement):
    stmts = parse_statements(driver)
    if driver.has_errors():
        return None
    loop_statement.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ELIF:
        return loop_statement
    elif peek_token.type_symbol == symbols.ELSE:
        return loop_statement
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, loop_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, loop_statement):
    driver.discard_token()
    return loop_statement


def enforce_loop(loop_token):
    if loop_token.type_symbol != symbols.LOOP:
        raise Exception("INTERNAL ERROR: expected loop statement, got " + loop_token.literal)