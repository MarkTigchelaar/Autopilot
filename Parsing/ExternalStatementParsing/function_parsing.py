import Tokenization.symbols as symbols
from Parsing.utils import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ExternalStatementParsing.function_header_parsing import parse_function_header
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from ASTComponents.ExternalComponents.function_statement import FunctionStatement

def parse_function(driver):
    header = parse_function_header(driver)
    if driver.has_errors():
        return None
    func_stmt = FunctionStatement()
    func_stmt.add_header(header)
    modifier_container = driver.get_modifier_container()
    func_stmt.add_public_token(modifier_container.get_public_token())
    func_stmt.add_acyclic_token(modifier_container.get_acyclic_token())
    func_stmt.add_inline_token(modifier_container.get_inline_token())
    header.add_public_token(modifier_container.get_public_token())
    header.add_acyclic_token(modifier_container.get_acyclic_token())
    header.add_inline_token(modifier_container.get_inline_token())
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.DO:
        return do_step(driver, func_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, func_stmt):
    driver.discard_token()
    if driver.is_unit_testing():
        statements = []
    else:
        statements = parse_statements(driver)
    if driver.has_errors():
        return None
    func_stmt.add_statements(statements)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.ENDSCOPE:
        return end_step(driver, func_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, func_stmt):
    driver.discard_token()
    return func_stmt
