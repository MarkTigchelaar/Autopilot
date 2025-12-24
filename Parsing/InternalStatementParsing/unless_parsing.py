import Tokenization.symbols as symbols
from Parsing.utils import (
    is_eof_type,
    is_eof_type
)
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from ASTComponents.InternalComponents.unless_statement import UnlessStatement

def parse_unless(driver):
    unless_token = driver.next_token()
    enforce_unless(unless_token)
    peek_token = driver.peek_token()
    unless_statement = UnlessStatement()
    unless_statement.add_descriptor_token(unless_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return expression_step(driver, unless_statement)


def expression_step(driver, unless_statement):
    exp_ast = parse_expression(driver)
    if exp_ast is None:
        return None
    elif driver.has_errors():
        return None
    unless_statement.add_expression(exp_ast)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.DO:
        return do_step(driver, unless_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, unless_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return statements_step(driver, unless_statement)


def statements_step(driver, unless_statement):
    if driver.is_unit_testing():
        stmts = []
    else:
        stmts = parse_statements(driver, True)
    if driver.has_errors():
        return None
    unless_statement.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.ENDSCOPE:
        return end_step(driver, unless_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, unless_statement):
    driver.discard_token()
    return unless_statement


def enforce_unless(unless_token):
    if unless_token.internal_type != symbols.UNLESS:
        raise Exception("INTERNAL ERROR: expected unless statement, got " + unless_token.literal)
