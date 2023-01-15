import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from Parsing.ASTComponents import ast_node_keys

def parse_defer(driver):
    type_token = driver.next_token()
    enforce_defer(type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    re_assign_stmt = parse_re_assignment(driver)
    if driver.has_errors():
        return None
    defer_stmt = driver.make_node(ast_node_keys.DEFER_STMT)
    defer_stmt.add_reassignment_statement(re_assign_stmt)
    return defer_stmt
    

def parse_re_assignment(driver):
    type_token = driver.peek_token()
    enforce_identifier(type_token)
    l_value = parse_expression(driver)
    if driver.has_errors():
        return None
    peek_token = driver.peek_token()
    re_assign_stmt = driver.make_node(ast_node_keys.REASSIGN_STMT)
    re_assign_stmt.add_l_value_exp(l_value)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_assignment_operator(peek_token):
        return assignment_operator_step(driver, re_assign_stmt)
    else:
        # could be just a method call, like thing.method()\n ... if ... do .. end etc
        return re_assign_stmt

def assignment_operator_step(driver, re_assign_stmt):
    assignment_token = driver.next_token()
    re_assign_stmt.add_assignment_token(assignment_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif not is_valid_expression_token(peek_token):
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    r_value = parse_expression(driver)
    if driver.has_errors():
        return None
    re_assign_stmt.add_r_value(r_value)
    return re_assign_stmt


def enforce_defer(type_token):
    if type_token.type_symbol != symbols.DEFER:
        raise Exception("INTERNAL ERROR: expected defer keyword, got " + type_token.literal)

def enforce_identifier(type_token):
    if type_token.type_symbol != symbols.IDENTIFIER:
        raise Exception("INTERNAL ERROR: expected identifier, got " + type_token.literal)
