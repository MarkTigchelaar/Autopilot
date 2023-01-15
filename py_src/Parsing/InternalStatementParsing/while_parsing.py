import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys


def parse_while(driver):
    while_token = driver.next_token()
    enforce_while(while_token)
    peek_token = driver.peek_token()
    while_statement = driver.make_node(ast_node_keys.WHILE_STMT)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return expression_step(driver, while_statement)


def expression_step(driver, while_statement):
    exp_ast = parse_expression(driver)
    if exp_ast is None:
        return None
    elif driver.has_errors():
        return None
    while_statement.add_expression(exp_ast)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, while_statement)
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, while_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def as_step(driver, while_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return loop_name_step(driver, while_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def loop_name_step(driver, while_statement):
    loop_name_token = driver.next_token()
    while_statement.add_loop_name(loop_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, while_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def do_step(driver, while_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return statements_step(driver, while_statement)


def statements_step(driver, while_statement):
    stmts = parse_statements(driver)
    if driver.has_errors():
        return None
    while_statement.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, while_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, while_statement):
    driver.discard_token()
    return while_statement


def enforce_while(while_token):
    if while_token.type_symbol != symbols.WHILE:
        raise Exception("INTERNAL ERROR: expected while statement, got " + while_token.literal)
