import Tokenization.symbols as symbols
from Parsing.utils import (
    is_eof_type,
    is_eof_type
)
from ErrorHandling.parsing_error_messages import *
from ASTComponents.InternalComponents.break_statement import BreakStatement

def parse_break(driver):
    break_token = driver.next_token()
    enforce_break(break_token)
    peek_token = driver.peek_token()
    break_statement = BreakStatement()
    break_statement.add_descriptor_token(break_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.LEFT_PAREN:
        return left_paren_step(driver, break_statement)
    else:
        return break_statement


def left_paren_step(driver, break_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return label_name_step(driver, break_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def label_name_step(driver, break_statement):
    label_name_token = driver.next_token()
    break_statement.add_label_name(label_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.RIGHT_PAREN:
        return right_paren_step(driver, break_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def right_paren_step(driver, break_statement):
    driver.discard_token()
    return break_statement


def enforce_break(break_token):
    if break_token.internal_type != symbols.BREAK:
        raise Exception("INTERNAL ERROR: expected break statement, got " + break_token.literal)
