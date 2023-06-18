import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys

def parse_else(driver):
    else_token = driver.next_token()
    enforce_else(else_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        else_stmt = statements_step(driver)
        if else_stmt:
            else_stmt.add_descriptor_token(else_token)
        return else_stmt


def statements_step(driver):
    else_statement = driver.make_node(ast_node_keys.ELSE_STMT)
    stmts = parse_statements(driver)
    if driver.has_errors():
        return None
    else_statement.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, else_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, else_statement):
    driver.discard_token()
    return else_statement


def enforce_else(else_token):
    if else_token.type_symbol != symbols.ELSE:
        raise Exception("INTERNAL ERROR: expected else statement, got " + else_token.literal)
