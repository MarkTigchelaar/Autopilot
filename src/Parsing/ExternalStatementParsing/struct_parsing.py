import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.ExternalStatementParsing.function_parsing import parse_function
from Parsing.ASTComponents import ast_node_keys

def parse_struct(driver):
    struct_token = driver.next_token()
    enforce_struct(struct_token)
    struct_stmt = driver.make_node(ast_node_keys.STRUCT_STMT)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
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
    elif peek_token.type_symbol == symbols.IS:
        return is_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.USES:
        return uses_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def is_step(driver, struct_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    field = driver.make_node(ast_node_keys.STRUCT_FIELD_STMT)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.PUB:
        return pub_field_step(driver, struct_stmt, field)
    # elif peek_token.type_symbol == symbols.ACYCLIC:
    #     return acyclic_field_step(driver, struct_stmt, field)
    # elif peek_token.type_symbol == symbols.INLINE:
    #     return inline_field_step(driver, struct_stmt, field)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
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
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return field_name_step(driver, struct_stmt, field)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

# def acyclic_field_step(driver, struct_stmt, field):
#     acyclic_token = driver.next_token()
#     field.add_acyclic_token(acyclic_token)
#     peek_token = driver.peek_token()
#     if is_eof_type(peek_token):
#         driver.add_error(peek_token, EOF_REACHED)
#         return None
#     elif peek_token.type_symbol == symbols.PUB:
#         return pub_field_step(driver, struct_stmt, field)
#     elif peek_token.type_symbol == symbols.IDENTIFIER:
#         return field_name_step(driver, struct_stmt, field)
#     else:
#         driver.add_error(peek_token, UNEXPECTED_TOKEN)
#         return None


# def inline_field_step(driver, struct_stmt, field):
#     inline_token = driver.next_token()
#     field.add_inline_token(inline_token)
#     peek_token = driver.peek_token()
#     if is_eof_type(peek_token):
#         driver.add_error(peek_token, EOF_REACHED)
#         return None
#     elif peek_token.type_symbol == symbols.PUB:
#         return pub_field_step(driver, struct_stmt, field)
#     elif peek_token.type_symbol == symbols.IDENTIFIER:
#         return field_name_step(driver, struct_stmt, field)
#     else:
#         driver.add_error(peek_token, UNEXPECTED_TOKEN)
#         return None

def field_name_step(driver, struct_stmt, field):
    field_name_token = driver.next_token()
    field.add_field_name(field_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.AS:
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
    elif peek_token.type_symbol == symbols.IDENTIFIER:
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
    elif peek_token.type_symbol == symbols.COMMA:
        return field_comma_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.ACYCLIC:
        return acyclic_function_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.PUB:
        return pub_function_step(driver, struct_stmt, None)
    elif peek_token.type_symbol == symbols.FUN:
        return function_step(driver, struct_stmt, None, None)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def field_comma_step(driver, struct_stmt):
    driver.discard_token()
    field = driver.make_node(ast_node_keys.STRUCT_FIELD_STMT)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.PUB:
        return pub_field_step(driver, struct_stmt, field)
    # elif peek_token.type_symbol == symbols.ACYCLIC:
    #     return acyclic_field_step(driver, struct_stmt, field)
    # elif peek_token.type_symbol == symbols.INLINE:
    #     return inline_field_step(driver, struct_stmt, field)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
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
    elif peek_token.type_symbol == symbols.PUB:
        return pub_function_step(driver, struct_stmt, acyclic_token)
    elif peek_token.type_symbol == symbols.FUN:
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
    elif peek_token.type_symbol == symbols.FUN:
        return function_step(driver, struct_stmt, pub_token, acyclic_token)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def function_step(driver, struct_stmt, public_token, acyclic_token):
    function = parse_function(driver)
    if driver.has_errors():
        return None
    function.add_acyclic_token(acyclic_token)
    function.add_public_token(public_token)
    struct_stmt.add_function(function)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.ACYCLIC:
        return acyclic_function_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.PUB:
        return pub_function_step(driver, struct_stmt, None)
    elif peek_token.type_symbol == symbols.FUN:
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
    elif peek_token.type_symbol == symbols.IDENTIFIER:
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
    elif peek_token.type_symbol == symbols.COMMA:
        return interface_comma_step(driver, struct_stmt)
    elif peek_token.type_symbol == symbols.IS:
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
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return interface_step(driver, struct_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

def end_step(driver, struct_stmt):
    driver.discard_token()
    return struct_stmt


def enforce_struct(struct_token):
    if struct_token.type_symbol != symbols.STRUCT:
        raise Exception("INTERNAL ERROR: expected struct statement, got " + struct_token.literal)
