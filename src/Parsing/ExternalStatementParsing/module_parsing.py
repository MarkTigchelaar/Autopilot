import symbols
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from ASTComponents import ast_node_keys

def parse_module(driver):
    token = driver.next_token()
    enforce_module(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        driver.discard_token()
        module_stmt = driver.make_node(ast_node_keys.MODULE)
        module_stmt.add_name(peek_token)
        return module_stmt
    else:
        driver.add_error(peek_token, INVALID_MODULE_NAME)
        return None

def enforce_module(token):
    if token.type_symbol != symbols.MODULE:
        raise Exception("INTERNAL ERROR: expected module, got " + token.literal)
