from keywords import is_primitive_type, is_operator, is_scope_keyword 
from keywords import is_external_keyword, is_internal_statement_keyword
from keywords import is_other_internal_keyword, is_parens_or_collection_keyword
from ErrorHandling.parsing_error_messages import *
import symbols

# Operator precedence
HASHLITERAL = 1
LOGICAL     = 2
COMPARISON  = 3
SUM         = 4
PRODUCT     = 5
EXPONENT    = 6
STRUCTFIELD = 7
PREFIX      = 8
POSTFIX     = 9
CALL        = 10

def is_primitive_literal(token):
    return is_primitive_type(token) and not is_primitive_type(token, True)

def passes_expression_name_token_check(driver, token):
    if is_external_keyword(token):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    elif is_internal_statement_keyword(token):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    elif is_scope_keyword(token):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    elif is_operator(token):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    elif is_primitive_type(token, True):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    elif is_other_internal_keyword(token, True):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    elif is_parens_or_collection_keyword(token):
        driver.add_error(token, INVALID_CONST_OR_VAR)
        return False
    else:
        return True

def is_valid_index_token(token):
    int_types = (symbols.INT, symbols.LONG)
    return is_primitive_literal(token) and token.type_symbol in int_types

def is_valid_expression_token(token):
    if token.type_symbol == symbols.CHAR:
        return True
    elif token.type_symbol == symbols.STRING:
        return True
    elif token.type_symbol == symbols.BOOL:
        return True
    elif token.type_symbol == symbols.INT:
        return True
    elif token.type_symbol == symbols.LONG:
        return True
    elif token.type_symbol == symbols.FLOAT:
        return True
    elif token.type_symbol == symbols.DOUBLE:
        return True
    elif token.type_symbol == symbols.LEFT_PAREN:
        return True
    elif token.type_symbol == symbols.IDENTIFIER:
        return True
    elif token.type_symbol == symbols.TRUE:
        return True
    elif token.type_symbol == symbols.FALSE:
        return True
    else:
        return False


def out_of_place_collection_token(token):
    if token.type_symbol == symbols.COMMA:
        return True
    elif token.type_symbol == symbols.RIGHT_BRACKET:
        return True
    elif token.type_symbol == symbols.RIGHT_BRACE:
        return True
    elif token.type_symbol == symbols.RIGHT_PAREN:
        return True
    else:
        return False


def find_infix_precedence(peek_token):
    if peek_token.type_symbol in (symbols.PLUS, symbols.MINUS):
        return SUM
    elif peek_token.type_symbol in (symbols.STAR, symbols.SLASH, symbols.MOD):
        return PRODUCT
    elif peek_token.type_symbol == symbols.CARROT:
        return EXPONENT
    elif peek_token.type_symbol == symbols.COLON:
        return HASHLITERAL
    elif peek_token.type_symbol in (symbols.LESS, symbols.LESS_EQUAL, symbols.GREATER, symbols.GREATER_EQUAL, symbols.EQUAL_EQUAL, symbols.BANG_EQUAL):
        return COMPARISON
    elif peek_token.type_symbol in (symbols.AND, symbols.NAND, symbols.NOR, symbols.OR, symbols.XOR, symbols.NOT):
        return LOGICAL
    elif peek_token.type_symbol == symbols.DOT:
        return STRUCTFIELD
    elif peek_token.type_symbol in (symbols.LEFT_PAREN, symbols.LEFT_BRACKET):
        return CALL
    else:
        return -1

def is_sum_type(token):
    return token.type_symbol in (symbols.PLUS, symbols.MINUS)

def is_product(token):
    return token.type_symbol in (symbols.STAR, symbols.SLASH, symbols.MOD)

def is_exponent(token):
    return token.type_symbol in (symbols.CARROT)

def is_hash_literal(token):
    return token.type_symbol in (symbols.COLON)

def is_comparison_operator(token):
    return token.type_symbol in (
        symbols.LESS, 
        symbols.LESS_EQUAL, 
        symbols.GREATER,
        symbols.GREATER_EQUAL, 
        symbols.EQUAL_EQUAL, 
        symbols.BANG_EQUAL
    )

def is_logical_operator(token):
    return token.type_symbol in (
        symbols.AND, 
        symbols.NAND, 
        symbols.OR,
        symbols.NOR, 
        symbols.XOR, 
        symbols.NOT
    )

def is_function_call(token):
    return token.type_symbol in (symbols.LEFT_PAREN)

def is_collection_access_by_index(token):
    return token.type_symbol in (symbols.LEFT_BRACKET)

def is_field_accessor_operator(token):
    return token.type_symbol in (symbols.DOT)

def get_collection_literal(delimiter_type):
    if delimiter_type == symbols.LEFT_BRACKET:
        return '['
    elif delimiter_type == symbols.RIGHT_BRACKET:
        return ']'
    elif delimiter_type == symbols.LEFT_BRACE:
        return '{'
    elif delimiter_type == symbols.RIGHT_BRACE:
        return '}'
    else:
        raise Exception("INTERNAL ERROR: unknown symbol type: " + delimiter_type)


def is_assignment_operator(token):
    if token.type_symbol == symbols.EQUAL:
        return True
    elif token.type_symbol == symbols.PLUS_EQUAL:
        return True
    elif token.type_symbol == symbols.MINUS_EQUAL:
        return True
    elif token.type_symbol == symbols.STAR_EQUAL:
        return True
    elif token.type_symbol == symbols.SLASH_EQUAL:
        return True
    elif token.type_symbol == symbols.CARROT_EQUAL:
        return True
    elif token.type_symbol == symbols.MOD_EQUAL:
        return True
    else:
        return False
