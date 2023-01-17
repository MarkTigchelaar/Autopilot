import symbols
from ..parsing_utilities import *
from keywords import is_eof_type, is_primitive_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ASTComponents import ast_node_keys


def parse_union(driver):
    token = driver.next_token()
    enforce_union(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return union_name_step(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def union_name_step(driver):
    union_name_token = driver.next_token()
    union_stmt = driver.make_node(ast_node_keys.UNION)
    union_stmt.add_name(union_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IS:
        return is_step(driver, union_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

    
def is_step(driver, union_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return union_list_item_name_step(driver, union_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def union_list_item_name_step(driver, union_stmt):
    item_name_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, union_stmt, item_name_token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def as_step(driver, union_stmt, item_name_token):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return union_list_item_type_step(driver, union_stmt, item_name_token)
    elif is_primitive_type(peek_token, True):
        return union_list_item_type_step(driver, union_stmt, item_name_token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def union_list_item_type_step(driver, union_stmt, item_name_token):
    type_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        union_stmt.add_item(item_name_token, type_token)
        return comma_step(driver, union_stmt)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        union_stmt.add_item(item_name_token, type_token)
        return end_step(driver, union_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def comma_step(driver, union_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return union_list_item_name_step(driver, union_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, union_stmt):
    driver.discard_token()
    return union_stmt


def enforce_union(token):
    if token.type_symbol != symbols.UNION:
        raise Exception("INTERNAL ERROR: expected union got " + token.literal)
