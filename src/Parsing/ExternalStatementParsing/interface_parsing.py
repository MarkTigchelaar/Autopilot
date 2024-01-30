import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ExternalStatementParsing.function_header_parsing import parse_function_header
from ASTComponents import ast_node_keys



def parse_interface(driver):
    interface_token = driver.next_token()
    enforce_interface(interface_token)
    peek_token = driver.peek_token()
    interface_stmt = driver.make_node(ast_node_keys.INTERFACE_DEFINE)
    modifier_container = driver.get_modifier_container()
    interface_stmt.add_public_token(modifier_container.get_public_token())
    interface_stmt.add_acyclic_token(modifier_container.get_acyclic_token())
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return interface_name_step(driver, interface_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def interface_name_step(driver, interface_stmt):
    name_token = driver.next_token()
    interface_stmt.add_name(name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IS:
        return is_step(driver, interface_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def is_step(driver, interface_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.FUN:
        return functions_step(driver, interface_stmt)
    elif peek_token.type_symbol == symbols.ACYCLIC:
        return functions_step(driver, interface_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def functions_step(driver, interface_stmt):
    fn_headers = list()
    while True:
        peek_token = driver.peek_token()
        if is_eof_type(peek_token):
            driver.add_error(peek_token, EOF_REACHED)
            return None
        if peek_token.type_symbol not in (symbols.FUN, symbols.ACYCLIC):
            break
        acyclic_token = None
        if peek_token.type_symbol == symbols.ACYCLIC:
            acyclic_token = peek_token
            driver.discard_token()
            peek_token = driver.peek_token()
        if peek_token.type_symbol == symbols.FUN:
            fn_header = parse_function_header(driver, False)
            if fn_header is None:
                return None
            fn_header.add_acyclic_field(acyclic_token)
            fn_header.set_as_public(True)
            fn_headers.append(fn_header)
            peek_token = driver.peek_token()
            if peek_token.type_symbol != symbols.ENDSCOPE:
                driver.add_error(peek_token, UNEXPECTED_TOKEN)
                return None
            else:
                driver.discard_token()
        elif is_eof_type(peek_token):
            driver.add_error(peek_token, EOF_REACHED)
            return None
        else:
            driver.add_error(peek_token, UNEXPECTED_TOKEN)
            return None
    if len(fn_headers) < 1:
        driver.add_error(peek_token, NO_FUNCTIONS_IN_INTERFACE)
        return None
    interface_stmt.add_function_headers(fn_headers)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, interface_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, interface_stmt):
    driver.discard_token()
    return interface_stmt


def enforce_interface(interface_token):
    if interface_token.type_symbol != symbols.INTERFACE:
        raise Exception("INTERNAL ERROR: expected interface statement, got " + interface_token.literal)
