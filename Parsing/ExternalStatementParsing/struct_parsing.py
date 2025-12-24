import Tokenization.symbols as symbols
from Parsing.utils import is_eof_type, is_primitive_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ExternalStatementParsing.function_parsing import parse_function
from ASTComponents.ExternalComponents.struct_statement import StructStatement, StructField

def parse_struct(driver):
    struct_token = driver.next_token()
    enforce_struct(struct_token)
    struct_stmt = StructStatement()
    modifier_container = driver.get_modifier_container()
    struct_stmt.add_public_token(modifier_container.get_public_token())
    struct_stmt.add_acyclic_token(modifier_container.get_acyclic_token())
    struct_stmt.add_inline_token(modifier_container.get_inline_token())
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return struct_name_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def struct_name_step(driver, struct_stmt):
    struct_name_token = driver.next_token()
    struct_stmt.add_name(struct_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IS:
        return is_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.USES:
        return uses_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def is_step(driver, struct_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    field = StructField()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.PUB:
        return pub_field_step(driver, struct_stmt, field)
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return field_name_step(driver, struct_stmt, field)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def pub_field_step(driver, struct_stmt, field):
    public_token = driver.next_token()
    field.add_public_token(public_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return field_name_step(driver, struct_stmt, field)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def field_name_step(driver, struct_stmt, field):
    field_name_token = driver.next_token()
    field.add_field_name(field_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.AS:
        return as_step(driver, struct_stmt, field)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def as_step(driver, struct_stmt, field):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return field_type_step(driver, struct_stmt, field)
    elif is_primitive_type(peek_token):
        return field_type_step(driver, struct_stmt, field)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def field_type_step(driver, struct_stmt, field):
    type_token = driver.next_token()
    field.add_type_token(type_token)
    struct_stmt.add_field(field)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.COMMA:
        return field_comma_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.ENDSCOPE:
        return end_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.ACYCLIC:
        return acyclic_function_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.PUB:
        return pub_function_step(driver, struct_stmt, None)
    elif peek_token.internal_type == symbols.FUN:
        return function_step(driver, struct_stmt, None, None)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def field_comma_step(driver, struct_stmt):
    driver.discard_token()
    field = StructField()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.PUB:
        return pub_field_step(driver, struct_stmt, field)
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return field_name_step(driver, struct_stmt, field)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def acyclic_function_step(driver, struct_stmt):
    acyclic_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.PUB:
        return pub_function_step(driver, struct_stmt, acyclic_token)
    elif peek_token.internal_type == symbols.FUN:
        return function_step(driver, struct_stmt, None, acyclic_token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def pub_function_step(driver, struct_stmt, acyclic_token):
    pub_token = driver.next_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.FUN:
        return function_step(driver, struct_stmt, pub_token, acyclic_token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_step(driver, struct_stmt, public_token, acyclic_token):
    driver.delete_modifier_container()
    mods = driver.get_modifier_container()
    mods.add_public_token(public_token)
    mods.add_acyclic_token(acyclic_token)
    function = parse_function(driver)
    if driver.has_errors():
        return None

    struct_stmt.add_function(function)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.ENDSCOPE:
        return end_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.ACYCLIC:
        return acyclic_function_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.PUB:
        return pub_function_step(driver, struct_stmt, None)
    elif peek_token.internal_type == symbols.FUN:
        return function_step(driver, struct_stmt, None, None)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def uses_step(driver, struct_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return interface_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def interface_step(driver, struct_stmt):
    interface_token = driver.next_token()
    struct_stmt.add_interface(interface_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.COMMA:
        return interface_comma_step(driver, struct_stmt)
    elif peek_token.internal_type == symbols.IS:
        return is_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def interface_comma_step(driver, struct_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return interface_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def end_step(driver, struct_stmt):
    driver.discard_token()
    return struct_stmt


def enforce_struct(struct_token):
    if struct_token.internal_type != symbols.STRUCT:
        raise Exception("INTERNAL ERROR: expected struct statement, got " + struct_token.literal)
