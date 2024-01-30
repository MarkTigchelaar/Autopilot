import symbols
from ..parsing_utilities import *
from keywords import is_eof_type, is_primitive_type
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from ASTComponents import ast_node_keys

def parse_assignment(driver):
    type_token = driver.next_token()
    enforce_assignment(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        assign_statement = driver.make_node(ast_node_keys.ASSIGN_EXP)
        assign_statement.add_let_or_var(type_token)
        return variable_step(driver, assign_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def variable_step(driver, assign_statement):
    name_token = driver.next_token()
    assign_statement.add_name(name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, assign_statement)
    elif peek_token.type_symbol == symbols.EQUAL:
        return equal_step(driver, assign_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def as_step(driver, assign_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_primitive_type(peek_token, True):
        return type_step(driver, assign_statement)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return type_step(driver, assign_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def type_step(driver, assign_statement):
    type_token = driver.next_token()
    assign_statement.add_type(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.EQUAL:
        return equal_step(driver, assign_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None    


def equal_step(driver, assign_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_valid_expression_token(peek_token):
        exp_ast = parse_expression(driver)
        if driver.has_errors():
            return None
        assign_statement.add_expression_value(exp_ast)
        return assign_statement
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None    


def enforce_assignment(token):
    if not (token.type_symbol == symbols.LET or token.type_symbol == symbols.VAR):
        raise Exception("INTERNAL ERROR: expected assignment statement (let or var), got " + token.literal)
