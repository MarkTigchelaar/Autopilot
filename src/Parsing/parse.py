import symbols
from .parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from routes import parse_enum, parse_union, parse_error, parse_import, parse_module, parse_define, parse_interface, parse_function, parse_unittest, parse_struct

class StatementRestrictionTracker:
    def __init__(self):
        self.seen_module = False
        self.import_and_define_not_allowed = False
    
    def module_seen(self):
        self.seen_module = True
    
    def has_seen_module(self):
        return self.seen_module

    def restrict_statements(self):
        self.import_and_define_not_allowed = True

    def def_import_not_allowed(self):
        return self.import_and_define_not_allowed


def parse_src(driver):
    restrictor = StatementRestrictionTracker()
    ast = list()
    peek_token = driver.peek_token()
    while not is_eof_type(peek_token):
        type_declaration = type_declarations(driver, restrictor)
        if driver.has_errors():
            return None
        if type_declaration:
            ast.append(type_declaration)
        peek_token = driver.peek_token()
    return ast


def type_declarations(driver, restrictor):
    peek_token = driver.peek_token()
    if peek_token.type_symbol == symbols.MODULE:
        return try_parse_module(driver, restrictor)
    elif peek_token.type_symbol == symbols.DEFINE:
        return try_parse_define(driver, restrictor)
    elif peek_token.type_symbol == symbols.IMPORT:
        return try_parse_import(driver, restrictor)
    else:
        restrictor.restrict_statements()
    if peek_token.type_symbol == symbols.ACYCLIC:
        return parse_acyclic_type(driver)
    elif peek_token.type_symbol == symbols.INLINE:
        return parse_inline_type(driver)
    elif peek_token.type_symbol == symbols.PUB:
        return parse_public_type(driver)
    elif peek_token.type_symbol == symbols.UNITTEST:
        return parse_unittest(driver)
    else:
        return parse_other_type(driver)


def try_parse_module(driver, restrictor):
    if restrictor.has_seen_module() or restrictor.def_import_not_allowed():
        peek_token = driver.peek_token()
        driver.add_error(peek_token, MOD_NOT_ALLOWED)
        return None
    restrictor.module_seen()
    return parse_module(driver)


def try_parse_define(driver, restrictor):
    if restrictor.def_import_not_allowed():
        peek_token = driver.peek_token()
        driver.add_error(peek_token, DEFINE_NOT_ALLOWED)
        return None
    return parse_define(driver)


def try_parse_import(driver, restrictor):
    if restrictor.def_import_not_allowed():
        peek_token = driver.peek_token()
        driver.add_error(peek_token, IMPORT_NOT_ALLOWED)
        return None
    return parse_import(driver)


def parse_acyclic_type(driver):
    acyclic_token = driver.next_token()
    peek_token = driver.peek_token()
    public_token = None
    if peek_token.type_symbol == symbols.PUB:
        public_token = driver.next_token()
        peek_token = driver.peek_token()
    
    ast_node = None
    if peek_token.type_symbol == symbols.INTERFACE:
        ast_node = parse_interface(driver)
    elif peek_token.type_symbol == symbols.STRUCT:
        ast_node = parse_struct(driver)
    elif peek_token.type_symbol == symbols.FUN:
        ast_node = parse_function(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)

    if driver.has_errors():
        return None
    ast_node.add_acyclic_token(acyclic_token)
    ast_node.add_public_token(public_token)
    return ast_node


def parse_inline_type(driver):
    inline_token = driver.next_token()
    peek_token = driver.peek_token()
    public_token = None
    if peek_token.type_symbol == symbols.PUB:
        public_token = driver.next_token()
        peek_token = driver.peek_token()
    
    ast_node = None
    if peek_token.type_symbol == symbols.STRUCT:
        ast_node = parse_struct(driver)
    elif peek_token.type_symbol == symbols.FUN:
        ast_node = parse_function(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)

    if driver.has_errors():
        return None
    ast_node.add_inline_token(inline_token)
    ast_node.add_public_token(public_token)
    return ast_node


def parse_public_type(driver):
    public_token = driver.next_token()
    ast_node = parse_other_type(driver)
    if driver.has_errors():
        return None
    ast_node.add_public_token(public_token)
    return ast_node


def parse_other_type(driver):
    peek_token = driver.peek_token()
    if peek_token.type_symbol == symbols.STRUCT:
        return parse_struct(driver)
    elif peek_token.type_symbol == symbols.FUN:
        return parse_function(driver)
    elif peek_token.type_symbol == symbols.INTERFACE:
        return parse_interface(driver)
    elif peek_token.type_symbol == symbols.ENUM:
        return parse_enum(driver)
    elif peek_token.type_symbol == symbols.UNION:
        return parse_union(driver)
    elif peek_token.type_symbol == symbols.ERROR:
        return parse_error(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
