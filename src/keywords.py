import symbols
from Tokenization.token import Token

# Assembles symbol information into queriable data
def is_keyword(token: Token) -> bool:
    return token.type_symbol in full_key_word_set()

def is_external_keyword(token: Token) -> bool:
    return token.type_symbol in external_keywords()

def is_internal_statement_keyword(token: Token) -> bool:
    return token.type_symbol in internal_statement_keywords()

def is_other_internal_keyword(token: Token, check_literal = False) -> bool:
    tok_type = token.type_symbol
    if check_literal:
        tok_type = token.literal.upper()
    return tok_type in other_internal_statement_keywords()

def is_scope_keyword(token: Token) -> bool:
    return token.type_symbol in scope_keywords()

def is_operator(token: Token) -> bool:
    return token.type_symbol in operator_keywords()

def is_primitive_type(token: Token, check_literal = False) -> bool:
    tok_type = token.type_symbol
    if check_literal:
        tok_type = token.literal.upper()
    return tok_type in primitive_type_keywords()

def is_eof_type(token: Token) -> bool:
    return token.type_symbol == symbols.EOF

def is_parens_or_collection_keyword(token: Token) -> bool:
    return token.type_symbol in collection_or_paren_type_keywords()

def is_general_collection_type(token: Token) -> bool:
    return token.type_symbol in linear_collection_type_keywords().update(key_value_collection_type_keywords())

def is_linear_collection_type(token: Token) -> bool:
    return token.type_symbol in linear_collection_type_keywords()

def is_key_value_collection_type(token: Token) -> bool:
    return token.type_symbol in key_value_collection_type_keywords()

def is_special_union_type(token: Token) -> bool:
    return token.type_symbol in special_union_type_keywords()


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
        symbols.IS
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
    return {
        symbols.LIST, 
        symbols.LINKEDLIST, 
        symbols.VECTOR, 
        symbols.STACK,
        symbols.SET, 
        symbols.HASHSET, 
        symbols.TREESET, 
        symbols.QUEUE,
        symbols.FIFOQUEUE,
        symbols.PRIORITYQUEUE,
        symbols.DEQUE
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

def keyword_literal_to_symbol_map():
    return {
        '(' : symbols.LEFT_PAREN,
        ')' : symbols.RIGHT_PAREN,
        '[' : symbols.LEFT_BRACKET,
        ']' : symbols.RIGHT_BRACKET,
        '{' : symbols.LEFT_BRACE,
        '}' : symbols.RIGHT_BRACE,
        ',' : symbols.COMMA,
        '+' : symbols.PLUS,
        '-' : symbols.MINUS,
        '*' : symbols.STAR,
        '/' : symbols.SLASH,
        '%' : symbols.MOD,
        '^' : symbols.CARROT,
        '!=' : symbols.BANG_EQUAL,
        '=' : symbols.EQUAL,
        '==' : symbols.EQUAL_EQUAL,
        '>' : symbols.LESS,
        '>=' : symbols.LESS_EQUAL,
        '<' : symbols.GREATER,
        '<=' : symbols.GREATER_EQUAL,
        'and' : symbols.AND,
        'nand' : symbols.NAND,
        'or' : symbols.OR,
        'xor' : symbols.XOR,
        'nor' : symbols.NOR,
        'not' : symbols.NOT,
        '+=' : symbols.PLUS_EQUAL,
        '-=' : symbols.MINUS_EQUAL,
        '*=' : symbols.STAR_EQUAL,
        '/=' : symbols.SLASH_EQUAL,
        '^=' : symbols.CARROT_EQUAL,
        '%=' : symbols.MOD_EQUAL,
        '.' : symbols.DOT,
        '..' : symbols.RANGE,
        ':' : symbols.COLON,
        'library' : symbols.LIBRARY,
        'module' : symbols.MODULE,
        'import' : symbols.IMPORT,
        'from' : symbols.FROM,
        'define' : symbols.DEFINE,
        'for' : symbols.FOR,
        'loop' : symbols.LOOP,
        'while' : symbols.WHILE,
        'continue' : symbols.CONTINUE,
        'break' : symbols.BREAK,
        'error' : symbols.ERROR,
        'if' : symbols.IF,
        'else' : symbols.ELSE,
        'elif' : symbols.ELIF,
        'unless' : symbols.UNLESS,
        'switch' : symbols.SWITCH,
        'case' : symbols.CASE,
        'default' : symbols.DEFAULT,
        'return' : symbols.RETURN,
        'do' : symbols.DO,
        'end' : symbols.ENDSCOPE,
        'pub' : symbols.PUB,
        'self' : symbols.SELF,
        'fun' : symbols.FUN,
        'inline' : symbols.INLINE,
        'interface' : symbols.INTERFACE,
        'uses' : symbols.USES,
        'enum' : symbols.ENUM,
        'struct' : symbols.STRUCT,
        'union' : symbols.UNION,
        'Map' : symbols.MAP,
        'Dictionary' : symbols.DICTIONARY,
        'HashMap' : symbols.HASHMAP,
        'List' : symbols.LIST,
        'LinkedList' : symbols.LINKEDLIST,
        'Vector' : symbols.VECTOR,
        'Set' : symbols.SET,
        'HashSet' : symbols.HASHSET,
        'TreeSet' : symbols.TREESET,
        'Stack' : symbols.STACK,
        'Queue' : symbols.QUEUE,
        'FifoQueue' : symbols.FIFOQUEUE,
        'PriorityQueue' : symbols.PRIORITYQUEUE,
        'Deque' : symbols.DEQUE,
        'Option' : symbols.OPTION,
        'Result' : symbols.RESULT,
        'assert' : symbols.ASSERT,
        'debug' : symbols.DEBUG,
        'unittest' : symbols.UNITTEST,
        'defer' : symbols.DEFER,
        'acyclic' : symbols.ACYCLIC,
        'as' : symbols.AS,
        'is' : symbols.IS,
        'in' : symbols.IN,
        'let' : symbols.LET,
        'var' : symbols.VAR,
        'int' : symbols.INT,
        'long' : symbols.LONG,
        'float' : symbols.FLOAT,
        'double' : symbols.DOUBLE,
        'char' : symbols.CHAR,
        'string' : symbols.STRING,
        'bool' : symbols.BOOL,
        'true' : symbols.TRUE,
        'false' : symbols.FALSE
    }
