import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ExternalStatementParsing.function_header_parsing import parse_function_header
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys

def parse_function(driver):
    header = parse_function_header(driver)
    if driver.has_errors():
        return None
    func_stmt = driver.make_node(ast_node_keys.FN_STMT)
    func_stmt.add_header(header)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, func_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, func_stmt):
    driver.discard_token()
    statements = parse_statements(driver)
    if driver.has_errors():
        return None
    func_stmt.add_statements(statements)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, func_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, func_stmt):
    driver.discard_token()
    return func_stmt
