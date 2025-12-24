import Tokenization.symbols as symbols
from Parsing.utils import (
    is_eof_type,
    is_eof_type,
    is_valid_expression_token
)
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from ASTComponents.InternalComponents.return_statement import ReturnStatement

def parse_return(driver):
    return_token = driver.next_token()
    enforce_return(return_token)
    peek_token = driver.peek_token()
    return_statement = ReturnStatement()
    return_statement.add_descriptor_token(return_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif is_valid_expression_token(peek_token):
        return expression_step(driver, return_statement)
    else:
        return return_statement


def expression_step(driver, return_statement):
    exp_ast = parse_expression(driver)
    if exp_ast is None:
        return None
    elif driver.has_errors():
        return None
    return_statement.add_expression(exp_ast)
    return return_statement


def enforce_return(return_token):
    if return_token.internal_type != symbols.RETURN:
        raise Exception("INTERNAL ERROR: expected return statement, got " + return_token.literal)
