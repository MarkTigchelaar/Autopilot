import symbols
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ASTComponents import ast_node_keys

def parse_error(driver):
    token = driver.next_token()
    enforce_error(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return error_name_step(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def error_name_step(driver):
    error_name_token = driver.next_token()
    error_stmt = driver.make_node(ast_node_keys.ERROR)
    error_stmt.add_name(error_name_token)
    modifier_container = driver.get_modifier_container()
    error_stmt.add_public_token(modifier_container.get_public_token())
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IS:
        return is_step(driver, error_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None    


def is_step(driver, error_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return error_list_item_step(driver, error_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def error_list_item_step(driver, error_stmt):
    error_item_name_token = driver.next_token()
    error_stmt.new_item(error_item_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        return comma_step(driver, error_stmt)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, error_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def comma_step(driver, error_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return error_list_item_step(driver, error_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, error_stmt):
    driver.discard_token()
    return error_stmt


def enforce_error(token):
    if token.type_symbol != symbols.ERROR:
        raise Exception("INTERNAL ERROR: expected enum got " + token.literal)
