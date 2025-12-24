from Parsing.ExternalStatementParsing.enum_parsing import parse_enum
from Parsing.ExternalStatementParsing.union_parsing import parse_union
from Parsing.ExternalStatementParsing.error_parsing import parse_error
from Parsing.ExternalStatementParsing.import_parsing import parse_import
from Parsing.ExternalStatementParsing.module_parsing import parse_module
from Parsing.ExternalStatementParsing.define_parsing import parse_define
from Parsing.ExternalStatementParsing.interface_parsing import parse_interface
from Parsing.ExternalStatementParsing.function_parsing import parse_function
from Parsing.ExternalStatementParsing.unittest_parsing import parse_unittest
from Parsing.ExternalStatementParsing.struct_parsing import parse_struct
import Tokenization.symbols as symbols
from Parsing.utils import (
    is_eof_type,
    is_eof_type
)
from ErrorHandling.parsing_error_messages import *

def parse_file(driver):
    restrictor = StatementRestrictionTracker()
    ast = list()
    peek_token = driver.peek_token()
    while not is_eof_type(peek_token):
        driver.delete_modifier_container()
        type_declaration = type_declarations(driver, restrictor)
        if driver.has_errors():
            return None
        if type_declaration:
            ast.append(type_declaration)
        peek_token = driver.peek_token()
    return ast


def type_declarations(driver, restrictor):
    peek_token = driver.peek_token()
    if peek_token.internal_type == symbols.MODULE:
        return try_parse_module(driver, restrictor)
    elif peek_token.internal_type == symbols.DEFINE:
        return try_parse_define(driver, restrictor)
    elif peek_token.internal_type == symbols.IMPORT:
        return try_parse_import(driver, restrictor)
    else:
        restrictor.restrict_statements()
    if peek_token.internal_type == symbols.ACYCLIC:
        return parse_acyclic_type(driver)
    elif peek_token.internal_type == symbols.INLINE:
        return parse_inline_type(driver)
    elif peek_token.internal_type == symbols.PUB:
        return parse_public_type(driver)
    elif peek_token.internal_type == symbols.UNITTEST:
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
    modifier_container = driver.get_modifier_container()
    modifier_container.add_acyclic_token(acyclic_token)
    peek_token = driver.peek_token()
    public_token = None
    if peek_token.internal_type == symbols.PUB:
        public_token = driver.next_token()
        peek_token = driver.peek_token()
    modifier_container.add_public_token(public_token)
    
    ast_node = None
    if peek_token.internal_type == symbols.INTERFACE:
        ast_node = parse_interface(driver)
    elif peek_token.internal_type == symbols.STRUCT:
        ast_node = parse_struct(driver)
    elif peek_token.internal_type == symbols.FUN:
        ast_node = parse_function(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)

    if driver.has_errors():
        return None
    return ast_node


def parse_inline_type(driver):
    inline_token = driver.next_token()
    modifier_container = driver.get_modifier_container()
    modifier_container.add_inline_token(inline_token)
    peek_token = driver.peek_token()
    public_token = None
    if peek_token.internal_type == symbols.PUB:
        public_token = driver.next_token()
        peek_token = driver.peek_token()
    modifier_container.add_public_token(public_token)
    ast_node = None
    if peek_token.internal_type == symbols.STRUCT:
        ast_node = parse_struct(driver)
    elif peek_token.internal_type == symbols.FUN:
        ast_node = parse_function(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)

    if driver.has_errors():
        return None
    return ast_node


def parse_public_type(driver):
    public_token = driver.next_token()
    modifier_container = driver.get_modifier_container()
    modifier_container.add_public_token(public_token)
    ast_node = parse_other_type(driver)
    if driver.has_errors():
        return None
    return ast_node


def parse_other_type(driver):
    peek_token = driver.peek_token()
    if peek_token.internal_type == symbols.STRUCT:
        return parse_struct(driver)
    elif peek_token.internal_type == symbols.FUN:
        return parse_function(driver)
    elif peek_token.internal_type == symbols.INTERFACE:
        return parse_interface(driver)
    elif peek_token.internal_type == symbols.ENUM:
        return parse_enum(driver)
    elif peek_token.internal_type == symbols.UNION:
        return parse_union(driver)
    elif peek_token.internal_type == symbols.ERROR:
        return parse_error(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None

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
