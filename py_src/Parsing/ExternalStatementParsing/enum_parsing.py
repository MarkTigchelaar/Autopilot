import symbols
from keywords import is_eof_type, is_primitive_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ASTComponents import ast_node_keys

def parse_enum(driver):
    token = driver.next_token()
    enforce_enum(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return enum_name_step(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def enum_name_step(driver):
    name_token = driver.next_token()
    enum_stmt = driver.make_node(ast_node_keys.ENUM)
    enum_stmt.add_name(name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IS:
        return is_step(driver, enum_stmt)
    elif peek_token.type_symbol == symbols.LEFT_PAREN:
        return open_paren_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def is_step(driver, enum_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return item_list_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, INVALID_ENUM_ITEM)
        return None


def open_paren_step(driver, enum_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return enum_type_step(driver, enum_stmt)
    elif is_primitive_type(peek_token):
        return enum_type_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None    
    

def enum_type_step(driver, enum_stmt):
    token = driver.next_token()
    enum_stmt.add_general_type(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        return close_paren_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def close_paren_step(driver, enum_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IS:
        return is_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def item_list_step(driver, enum_stmt):
    item_name_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        enum_stmt.new_item(item_name_token, None)
        return comma_step(driver, enum_stmt)
    elif peek_token.type_symbol == symbols.EQUAL:
        return equal_step(driver, enum_stmt, item_name_token)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        enum_stmt.new_item(item_name_token, None)
        return end_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def comma_step(driver, enum_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return item_list_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def equal_step(driver, enum_stmt, item_name_token):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return item_list_literal_step(driver, enum_stmt, item_name_token)
    elif is_primitive_type(peek_token):
        return item_list_literal_step(driver, enum_stmt, item_name_token)
    elif peek_token.type_symbol == symbols.MINUS:
        return item_list_literal_step(driver, enum_stmt, item_name_token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def item_list_literal_step(driver, enum_stmt, item_name_token):
    token = driver.next_token()
    peek_token = driver.peek_token()
    if token.type_symbol == symbols.MINUS:
        if peek_token.type_symbol == symbols.IDENTIFIER:
            token.literal += peek_token.literal
            enum_stmt.new_item(item_name_token, token)
        elif is_primitive_type(peek_token):
            token.literal += peek_token.literal
            enum_stmt.new_item(item_name_token, token)
        elif is_eof_type(peek_token):
            driver.add_error(peek_token, EOF_REACHED)
            return None
        else:
            driver.add_error(peek_token, UNEXPECTED_TOKEN)
            return None
    elif token.type_symbol == symbols.IDENTIFIER:
        enum_stmt.new_item(item_name_token, token)
    elif is_primitive_type(token):
        enum_stmt.new_item(item_name_token, token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.COMMA:
        return comma_step(driver, enum_stmt)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, enum_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def end_step(driver, enum_stmt):
    driver.discard_token()
    return enum_stmt

def enforce_enum(token):
    if token.type_symbol != symbols.ENUM:
        raise Exception("INTERNAL ERROR: expected enum got " + token.literal)
