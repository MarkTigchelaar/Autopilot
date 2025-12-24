from Tokenization.token import Token
from Tokenization import symbols
from ErrorHandling.parsing_error_messages import (
    INVALID_CONST_OR_VAR,
)


# Operator precedence
HASHLITERAL = 1
LOGICAL = 2
COMPARISON = 3
SUM = 4
PRODUCT = 5
EXPONENT = 6
STRUCTFIELD = 7
PREFIX = 8
POSTFIX = 9
CALL = 10

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
    return is_primitive_literal(token) and token.internal_type in int_types

# Does the left most token start with one of the following?
def is_valid_expression_token(token, include_prefixes = True):
    if token.internal_type == symbols.CHAR:
        return True
    elif token.internal_type == symbols.STRING:
        return True
    elif token.internal_type == symbols.BOOL:
        return True
    elif token.internal_type == symbols.INT:
        return True
    elif token.internal_type == symbols.LONG:
        return True
    elif token.internal_type == symbols.FLOAT:
        return True
    elif token.internal_type == symbols.DOUBLE:
        return True
    elif token.internal_type == symbols.LEFT_PAREN:
        return True
    elif token.internal_type == symbols.LEFT_BRACE:
        return True
    elif token.internal_type == symbols.LEFT_BRACKET:
        return True
    elif token.internal_type == symbols.IDENTIFIER:
        return True
    elif token.internal_type == symbols.TRUE:
        return True
    elif token.internal_type == symbols.FALSE:
        return True
    elif token.internal_type == symbols.MINUS:
        return True and include_prefixes
    elif token.internal_type == symbols.NOT:
        return True and include_prefixes
    else:
        return False


def out_of_place_collection_token(token):
    if token.internal_type == symbols.COMMA:
        return True
    elif token.internal_type == symbols.RIGHT_BRACKET:
        return True
    elif token.internal_type == symbols.RIGHT_BRACE:
        return True
    elif token.internal_type == symbols.RIGHT_PAREN:
        return True
    else:
        return False


def find_infix_precedence(peek_token):
    if peek_token.internal_type in (symbols.PLUS, symbols.MINUS):
        return SUM
    elif peek_token.internal_type in (symbols.STAR, symbols.SLASH, symbols.MOD):
        return PRODUCT
    elif peek_token.internal_type == symbols.CARROT:
        return EXPONENT
    elif peek_token.internal_type == symbols.COLON:
        return HASHLITERAL
    elif peek_token.internal_type in (
        symbols.LESS,
        symbols.LESS_EQUAL,
        symbols.GREATER,
        symbols.GREATER_EQUAL,
        symbols.EQUAL_EQUAL,
        symbols.BANG_EQUAL,
    ):
        return COMPARISON
    elif peek_token.internal_type in (
        symbols.AND,
        symbols.NAND,
        symbols.NOR,
        symbols.OR,
        symbols.XOR,
        symbols.NOT,
    ):
        return LOGICAL
    elif peek_token.internal_type == symbols.DOT:
        return STRUCTFIELD
    elif peek_token.internal_type in (symbols.LEFT_PAREN, symbols.LEFT_BRACKET):
        return CALL
    else:
        return -1


def is_sum_type(token):
    return token.internal_type in (symbols.PLUS, symbols.MINUS)


def is_product(token):
    return token.internal_type in (symbols.STAR, symbols.SLASH, symbols.MOD)


def is_exponent(token):
    return token.internal_type in (symbols.CARROT)


def is_hash_literal(token):
    return token.internal_type in (symbols.COLON)


def is_comparison_operator(token):
    return token.internal_type in (
        symbols.LESS,
        symbols.LESS_EQUAL,
        symbols.GREATER,
        symbols.GREATER_EQUAL,
        symbols.EQUAL_EQUAL,
        symbols.BANG_EQUAL,
    )


def is_logical_operator(token):
    return token.internal_type in (
        symbols.AND,
        symbols.NAND,
        symbols.OR,
        symbols.NOR,
        symbols.XOR,
        symbols.NOT,
    )

def is_prefix_logical_operator(token):
    return token.internal_type == symbols.NOT


def is_function_call(token):
    return token.internal_type in (symbols.LEFT_PAREN)


def is_collection_access_by_index(token):
    return token.internal_type in (symbols.LEFT_BRACKET)


def is_field_accessor_operator(token):
    return token.internal_type in (symbols.DOT)


def get_collection_literal(delimiter_type):
    if delimiter_type == symbols.LEFT_BRACKET:
        return "["
    elif delimiter_type == symbols.RIGHT_BRACKET:
        return "]"
    elif delimiter_type == symbols.LEFT_BRACE:
        return "{"
    elif delimiter_type == symbols.RIGHT_BRACE:
        return "}"
    else:
        raise Exception("INTERNAL ERROR: unknown symbol type: " + delimiter_type)


def is_assignment_operator(token):
    if token.internal_type == symbols.EQUAL:
        return True
    elif token.internal_type == symbols.PLUS_EQUAL:
        return True
    elif token.internal_type == symbols.MINUS_EQUAL:
        return True
    elif token.internal_type == symbols.STAR_EQUAL:
        return True
    elif token.internal_type == symbols.SLASH_EQUAL:
        return True
    elif token.internal_type == symbols.CARROT_EQUAL:
        return True
    elif token.internal_type == symbols.MOD_EQUAL:
        return True
    else:
        return False


def is_keyword(token: Token) -> bool:
    return token.internal_type in full_key_word_set()

def is_external_keyword(token: Token) -> bool:
    return token.internal_type in external_keywords()

def is_internal_statement_keyword(token: Token) -> bool:
    return token.internal_type in internal_statement_keywords()

def is_other_internal_keyword(token: Token, check_literal = False) -> bool:
    tok_type = token.internal_type
    if check_literal:
        tok_type = token.literal.upper()
    return tok_type in other_internal_statement_keywords()

def is_scope_keyword(token: Token) -> bool:
    return token.internal_type in scope_keywords()

def is_operator(token: Token) -> bool:
    return token.internal_type in operator_keywords()

def is_primitive_type(token: Token, check_literal = False) -> bool:
    if token is None:
        return False
    tok_type = token.internal_type
    if check_literal:
        tok_type = token.literal.upper()
    return tok_type in primitive_type_keywords()

def is_eof_type(token: Token) -> bool:
    return token.internal_type == symbols.EOF

def is_parens_or_collection_keyword(token: Token) -> bool:
    return token.internal_type in collection_or_paren_type_keywords()

# def is_general_collection_type(token: Token) -> bool:
#     return token.internal_type in linear_collection_type_keywords().update(key_value_collection_type_keywords())

def is_list_collection_type(token: Token) -> bool:
    return token.internal_type in list_collection_type_keywords()

def is_hash_collection_type(token: Token) -> bool:
    return token.internal_type in hash_collection_type_keywords()

def is_queue_collection_type(token: Token) -> bool:
    return token.internal_type in queue_collection_type_keywords()

def is_key_value_collection_type(token: Token) -> bool:
    return token.internal_type in key_value_collection_type_keywords()

def is_special_union_type(token: Token) -> bool:
    return token.internal_type in special_union_type_keywords()

def is_boolean_literal(token: Token) -> bool:
    return token.internal_type in boolean_keywords()

def collection_or_paren_type_keywords() -> set:
    collections = collection_delimiter_keywords()
    collections.update(grouping_type_keywords())
    return collections

def full_key_word_set() -> set:
    keywords = set()
    keywords.update(boolean_keywords())
    keywords.update(operator_keywords())
    keywords.update(external_keywords())
    keywords.update(function_def())
    keywords.update(scope_keywords())
    keywords.update(internal_statement_keywords())
    keywords.update(primitive_type_keywords())
    keywords.update(other_internal_statement_keywords())
    keywords.update(collection_or_paren_type_keywords())
    keywords.update(linear_collection_type_keywords())
    keywords.update(key_value_collection_type_keywords())
    keywords.update(special_union_type_keywords())
    keywords.update(misc_keywords())
    return keywords


def boolean_keywords() -> set:
    return {symbols.TRUE, symbols.FALSE}

def combined_assignment_operators() -> set:
    return {
        symbols.PLUS_EQUAL,
        symbols.MINUS_EQUAL,
        symbols.STAR_EQUAL,
        symbols.SLASH_EQUAL,
        symbols.CARROT_EQUAL,
        symbols.MOD_EQUAL
    }

def boolean_operators() -> set:
    return {
        symbols.AND,
        symbols.NAND,
        symbols.OR,
        symbols.XOR,
        symbols.NOR,
        symbols.NOT
    }

def comparison_operators() -> set:
    return {
        symbols.BANG_EQUAL,
        symbols.EQUAL_EQUAL,
        symbols.GREATER,
        symbols.GREATER_EQUAL,
        symbols.LESS,
        symbols.LESS_EQUAL
    }

def assignment_operators() -> set:
    return {
        symbols.EQUAL
    }

def function_def() -> set:
    return {symbols.FUN}

def scope_keywords() -> set:
    return {
        symbols.DO,
        symbols.ENDSCOPE
    }

def external_keywords() -> set:
    return {
        symbols.MODULE,
        symbols.LIBRARY,
        symbols.FROM,
        symbols.IMPORT,
        symbols.DEFINE,
        symbols.UNITTEST,
        symbols.FUN,
        symbols.INTERFACE,
        symbols.ENUM,
        symbols.ACYCLIC,
        symbols.UNION,  
        symbols.ERROR,
        symbols.STRUCT,
        symbols.INLINE,
        symbols.IS,
        symbols.PUB
    }

def internal_statement_keywords() -> set:
    return {
        symbols.IF,
        symbols.ELIF,
        symbols.ELSE,
        symbols.UNLESS,
        symbols.SWITCH,
        symbols.CASE,
        symbols.DEFAULT,
        symbols.DEFER,
        symbols.RETURN,
        symbols.FOR,
        symbols.LOOP,
        symbols.WHILE,
        symbols.CONTINUE,
        symbols.BREAK
    }

def other_internal_statement_keywords() -> set:
    return {
        symbols.LET,
        symbols.VAR,
        symbols.IN,
        symbols.AS
    }

def operator_keywords() -> set:
    operators = set()
    operators.update(boolean_operators())
    operators.update(combined_assignment_operators())
    operators.update(comparison_operators())
    operators.update(assignment_operators())
    operators.update(math_operators())
    operators.update(field_access_keywords())
    operators.update(range_access_keywords())
    return operators

def field_access_keywords() -> set:
    return {
        symbols.DOT
    }

def range_access_keywords() ->set:
    return {
        symbols.RANGE
    }

def primitive_type_keywords() -> set:
    return {
        symbols.INT,
        symbols.LONG,
        symbols.FLOAT,
        symbols.DOUBLE,
        symbols.CHAR,
        symbols.STRING,
        symbols.BOOL
    }

def math_operators() -> set:
    return {
        symbols.PLUS,
        symbols.MINUS,
        symbols.SLASH,
        symbols.STAR,
        symbols.CARROT,
        symbols.MOD
    }

def grouping_type_keywords() -> set:
    return {
        symbols.LEFT_PAREN,
        symbols.RIGHT_PAREN
    }

def collection_delimiter_keywords() -> set:
    return {
        symbols.LEFT_BRACE,
        symbols.LEFT_BRACKET,
        symbols.RIGHT_BRACE,
        symbols.RIGHT_BRACKET
    }

def linear_collection_type_keywords() -> set:
    types = set()
    types.update(list_collection_type_keywords())
    types.update(hash_collection_type_keywords())
    types.update(queue_collection_type_keywords())
    types.update(stack_collection_type_keywords())
    return types

def list_collection_type_keywords() -> set:
    return {
        symbols.LIST, 
        symbols.LINKEDLIST, 
        symbols.VECTOR
    }

def hash_collection_type_keywords() -> set:
    return {
        symbols.SET, 
        symbols.HASHSET, 
        symbols.TREESET
    }

def queue_collection_type_keywords() -> set:
    return {
        symbols.QUEUE,
        symbols.FIFOQUEUE,
        symbols.PRIORITYQUEUE,
        symbols.DEQUE
    }

def stack_collection_type_keywords() -> set:
    return {
        symbols.STACK
    }

def key_value_collection_type_keywords() -> set:
    return {
        symbols.DICTIONARY,
        symbols.HASHMAP,
        symbols.MAP
    }

def special_union_type_keywords() -> set:
    return {
        symbols.OPTION,
        symbols.RESULT
    }

def misc_keywords() -> set:
    return { 
        symbols.USES,
        symbols.DEBUG,
        symbols.ASSERT,
        symbols.SELF,
        symbols.PUB
    }

# def keyword_literal_to_symbol_map():
#     return {
#         '(' : symbols.LEFT_PAREN,
#         ')' : symbols.RIGHT_PAREN,
#         '[' : symbols.LEFT_BRACKET,
#         ']' : symbols.RIGHT_BRACKET,
#         '{' : symbols.LEFT_BRACE,
#         '}' : symbols.RIGHT_BRACE,
#         ',' : symbols.COMMA,
#         '+' : symbols.PLUS,
#         '-' : symbols.MINUS,
#         '*' : symbols.STAR,
#         '/' : symbols.SLASH,
#         '%' : symbols.MOD,
#         '^' : symbols.CARROT,
#         '!=' : symbols.BANG_EQUAL,
#         '=' : symbols.EQUAL,
#         '==' : symbols.EQUAL_EQUAL,
#         '>' : symbols.LESS,
#         '>=' : symbols.LESS_EQUAL,
#         '<' : symbols.GREATER,
#         '<=' : symbols.GREATER_EQUAL,
#         'and' : symbols.AND,
#         'nand' : symbols.NAND,
#         'or' : symbols.OR,
#         'xor' : symbols.XOR,
#         'nor' : symbols.NOR,
#         'not' : symbols.NOT,
#         '+=' : symbols.PLUS_EQUAL,
#         '-=' : symbols.MINUS_EQUAL,
#         '*=' : symbols.STAR_EQUAL,
#         '/=' : symbols.SLASH_EQUAL,
#         '^=' : symbols.CARROT_EQUAL,
#         '%=' : symbols.MOD_EQUAL,
#         '.' : symbols.DOT,
#         '..' : symbols.RANGE,
#         ':' : symbols.COLON,
#         'library' : symbols.LIBRARY,
#         'module' : symbols.MODULE,
#         'import' : symbols.IMPORT,
#         'from' : symbols.FROM,
#         'define' : symbols.DEFINE,
#         'for' : symbols.FOR,
#         'loop' : symbols.LOOP,
#         'while' : symbols.WHILE,
#         'continue' : symbols.CONTINUE,
#         'break' : symbols.BREAK,
#         'error' : symbols.ERROR,
#         'if' : symbols.IF,
#         'else' : symbols.ELSE,
#         'elif' : symbols.ELIF,
#         'unless' : symbols.UNLESS,
#         'switch' : symbols.SWITCH,
#         'case' : symbols.CASE,
#         'default' : symbols.DEFAULT,
#         'return' : symbols.RETURN,
#         'do' : symbols.DO,
#         'end' : symbols.ENDSCOPE,
#         'pub' : symbols.PUB,
#         'self' : symbols.SELF,
#         'fun' : symbols.FUN,
#         'inline' : symbols.INLINE,
#         'interface' : symbols.INTERFACE,
#         'uses' : symbols.USES,
#         'enum' : symbols.ENUM,
#         'struct' : symbols.STRUCT,
#         'union' : symbols.UNION,
#         'Map' : symbols.MAP,
#         'Dictionary' : symbols.DICTIONARY,
#         'HashMap' : symbols.HASHMAP,
#         'List' : symbols.LIST,
#         'LinkedList' : symbols.LINKEDLIST,
#         'Vector' : symbols.VECTOR,
#         'Set' : symbols.SET,
#         'HashSet' : symbols.HASHSET,
#         'TreeSet' : symbols.TREESET,
#         'Stack' : symbols.STACK,
#         'Queue' : symbols.QUEUE,
#         'FifoQueue' : symbols.FIFOQUEUE,
#         'PriorityQueue' : symbols.PRIORITYQUEUE,
#         'Deque' : symbols.DEQUE,
#         'Option' : symbols.OPTION,
#         'Result' : symbols.RESULT,
#         'assert' : symbols.ASSERT,
#         'debug' : symbols.DEBUG,
#         'unittest' : symbols.UNITTEST,
#         'defer' : symbols.DEFER,
#         'acyclic' : symbols.ACYCLIC,
#         'as' : symbols.AS,
#         'is' : symbols.IS,
#         'in' : symbols.IN,
#         'let' : symbols.LET,
#         'var' : symbols.VAR,
#         'int' : symbols.INT,
#         'long' : symbols.LONG,
#         'float' : symbols.FLOAT,
#         'double' : symbols.DOUBLE,
#         'char' : symbols.CHAR,
#         'string' : symbols.STRING,
#         'bool' : symbols.BOOL,
#         'true' : symbols.TRUE,
#         'false' : symbols.FALSE
#     }


class AstContainer:
    def __init__(self):
        self.node_list = list()
    
    def add_ast_for_file(self, ast, filename):
        node = AstNode(filename, ast)
        self.add_node(node)

    def add_node(self, node):
        self.node_list.append(node)

class AstNode:
    def __init__(self, filename, ast):
        self.filename = filename
        self.ast = ast