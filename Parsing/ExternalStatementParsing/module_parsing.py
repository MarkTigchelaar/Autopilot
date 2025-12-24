import Tokenization.symbols as symbols
from ErrorHandling.parsing_error_messages import *
from Parsing.utils import is_eof_type
from ASTComponents.ExternalComponents.module_statement import ModuleStatement

def parse_module(driver):
    token = driver.next_token()
    enforce_module(token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        driver.discard_token()
        module_stmt = ModuleStatement()
        module_stmt.add_name(peek_token)
        return module_stmt
    else:
        driver.add_error(peek_token, INVALID_MODULE_NAME)
        return None

def enforce_module(token):
    if token.internal_type != symbols.MODULE:
        raise Exception("INTERNAL ERROR: expected module, got " + token.literal)
