import symbols
from keywords import is_eof_type, is_keyword
from ErrorHandling.parsing_error_messages import *
from Parsing.ASTComponents import ast_node_keys


def parse_import(driver):
    token = driver.next_token()
    enforce_import(token)
    peek_token = driver.peek_token()
    import_stmt = driver.make_node(ast_node_keys.IMPORT)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.type_symbol == symbols.MODULE:
        return module_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.LIBRARY:
        return library_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return import_list_item_step(driver, import_stmt)
    else:
        driver.add_error(peek_token, INVALID_IMPORT_ITEM)
        return None


def module_step(driver, import_stmt):
    import_stmt.set_as_module()
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return module_name_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.RANGE:
        return module_path_step(driver, import_stmt, None)
    elif peek_token.type_symbol == symbols.CARROT:
        return module_path_step(driver, import_stmt, None)
    else:
        driver.add_error(peek_token, INVALID_IMPORTED_MODULE_NAME)
        return None
    
def library_step(driver, import_stmt):
    import_stmt.set_as_library()
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return module_name_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.RANGE:
        return module_path_step(driver, import_stmt, None)
    elif peek_token.type_symbol == symbols.CARROT:
        return module_path_step(driver, import_stmt, None)
    else:
        driver.add_error(peek_token, INVALID_IMPORTED_MODULE_NAME)
        return None


def import_list_item_step(driver, import_stmt):
    token = driver.next_token()
    if is_eof_type(token):
        driver.add_error(token, EOF_REACHED)
        return None
    
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
        return as_step(driver, import_stmt, token)
    elif peek_token.type_symbol == symbols.FROM:
        import_stmt.new_import_item(token, None)
        return from_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.COMMA:
        import_stmt.new_import_item(token, None)
        return comma_step(driver, import_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def as_step(driver, import_stmt, item_name_token):
    driver.discard_token()
    peek_name_token = driver.peek_token()
    if is_eof_type(peek_name_token):
        driver.add_error(peek_name_token, EOF_REACHED)
        return None
    elif peek_name_token.type_symbol == symbols.IDENTIFIER:
        return import_item_alias_step(driver, import_stmt, item_name_token)
    else:
        driver.add_error(peek_name_token, INVALID_IMPORT_ITEM)
        return None


def import_item_alias_step(driver, import_stmt, item_name_token):
    new_name_token = driver.next_token()
    import_stmt.new_import_item(item_name_token, new_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.FROM:
        return from_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.COMMA:
        return comma_step(driver, import_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def from_step(driver, import_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.MODULE:
        return module_step(driver, import_stmt)
    elif peek_token.type_symbol == symbols.LIBRARY:
        return library_step(driver, import_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def comma_step(driver, import_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return import_list_item_step(driver, import_stmt)
    elif is_keyword(peek_token):
        driver.add_error(peek_token, INVALID_IMPORT_ITEM)
        return None
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def module_name_step(driver, import_stmt):
    name_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        import_stmt.new_path_item(name_token, None)
        return import_stmt
    elif peek_token.type_symbol == symbols.DOT:
        return module_path_step(driver, import_stmt, name_token)
    elif peek_token.type_symbol == symbols.RANGE:
        return module_path_step(driver, import_stmt, name_token)
    elif peek_token.type_symbol == symbols.COLON:
        return module_path_step(driver, import_stmt, name_token)
    elif peek_token.type_symbol == symbols.CARROT:
        return module_path_step(driver, import_stmt, None)
    else:
        import_stmt.new_path_item(name_token, None)
        return import_stmt


def module_path_step(driver, import_stmt, name_token):
    next_token = driver.next_token()
    peek_token = driver.peek_token()
    import_stmt.new_path_item(name_token, next_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return module_name_step(driver, import_stmt)
    else:
        driver.add_error(peek_token, INVALID_IMPORTED_MODULE_NAME)
        return None


def enforce_import(token):
    if token.type_symbol != symbols.IMPORT:
        raise Exception("INTERNAL ERROR: expected import, got " + token.literal)
