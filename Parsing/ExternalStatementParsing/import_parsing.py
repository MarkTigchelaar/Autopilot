import Tokenization.symbols as symbols
from Parsing.utils import is_eof_type, is_keyword, is_external_keyword
from ErrorHandling.parsing_error_messages import *
from ASTComponents.ExternalComponents.import_statement import ImportStatement

# import thing_one as one, thing_two from module items


def parse_import(driver):
    token = driver.next_token()
    enforce_import(token)
    peek_token = driver.peek_token()
    import_stmt = ImportStatement()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif driver.has_errors():
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return module_name_step(driver, import_stmt)
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return module_name_step(driver, import_stmt)
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
    elif peek_token.internal_type == symbols.AS:
        return as_step(driver, import_stmt, token)
    elif peek_token.internal_type == symbols.FROM:
        import_stmt.new_import_item(token, None)
        return from_step(driver, import_stmt)
    elif peek_token.internal_type == symbols.COMMA:
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
    elif peek_name_token.internal_type == symbols.IDENTIFIER:
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
    elif peek_token.internal_type == symbols.FROM:
        return from_step(driver, import_stmt)
    elif peek_token.internal_type == symbols.COMMA:
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
    elif peek_token.internal_type == symbols.MODULE:
        return module_step(driver, import_stmt)
    elif peek_token.internal_type == symbols.LIBRARY:
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
    elif peek_token.internal_type == symbols.IDENTIFIER:
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
    import_stmt.set_source_name(name_token)
    if is_eof_type(peek_token):
        return import_stmt
    elif peek_token.internal_type == symbols.LOCATION:
        if import_stmt.import_type == "library":
            driver.add_error(peek_token, LIBRARY_WITH_PATH)
            return None
        return location_step(driver, import_stmt)
    elif peek_token.internal_type in (symbols.DOT, symbols.RANGE, symbols.COLON, symbols.CARROT):
        driver.add_error(peek_token, INVALID_IMPORT_PATH)
        return None
    else:
        return import_stmt


def location_step(driver, import_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()

    if peek_token.internal_type == symbols.DOT:
        return import_path_direction_step(driver, import_stmt)
    elif peek_token.internal_type == symbols.RANGE:
        return import_path_direction_step(driver, import_stmt)
    elif peek_token.internal_type == symbols.COLON:
        return import_path_direction_step(driver, import_stmt)
    elif peek_token.internal_type == symbols.CARROT:
        return import_path_direction_step(driver, import_stmt)
    else:
        driver.add_error(peek_token, INVALID_IMPORT_PATH)
        return None


def import_path_direction_step(driver, import_stmt):
    direction_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return import_path_folder_name_step(driver, import_stmt, direction_token)
    else:
        driver.add_error(peek_token, INVALID_IMPORT_PATH)
        return None


def import_path_folder_name_step(driver, import_stmt, direction_token):
    folder_name_token = driver.next_token()
    import_stmt.new_path_item(folder_name_token, direction_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        return import_stmt
    elif is_external_keyword(peek_token):
        return import_stmt
    else:
        return import_path_direction_step(driver, import_stmt)


def enforce_import(token):
    if token.internal_type != symbols.IMPORT:
        raise Exception("INTERNAL ERROR: expected import, got " + token.literal)
