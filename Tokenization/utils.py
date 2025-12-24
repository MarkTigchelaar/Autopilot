from typing import Union
import Tokenization.symbols as symbols

def is_digit(char: Union[str, None]) -> bool:
    if empty_char(char):
        return False
    return ((char >= "0") and (char <= "9"))

def is_alpha(char: Union[str, None]) -> bool:
    if empty_char(char):
        return False
    is_lower = char >= 'a' and char <= 'z'
    is_upper = char >= 'A' and char <= 'Z'
    return (is_lower or is_upper or char == '_')

def is_alpha_numeric(char: Union[str, None]) -> bool:
    return is_digit(char) or is_alpha(char)

def is_special_char(char: Union[str, None]) -> bool:
    if empty_char(char):
        return False
    return char in ["@", "$", "_" , "~", "#", "&", ";", "?", "!"]

def empty_char(char: Union[str, None]) -> bool:
    return char in (None, "")


def get_file_path_and_file_name(full_file_name: str) -> tuple[str, str]:
    if full_file_name.rfind("/") != -1:
        last_slash = full_file_name.rfind("/")
        file_name = full_file_name[last_slash + 1 :]
        file_path = full_file_name[: last_slash + 1]
    elif full_file_name.rfind("/") != -1:
        last_slash = full_file_name.rfind("/")
        file_name = full_file_name[last_slash + 1 :]
        file_path = full_file_name[: last_slash + 1]
    elif full_file_name.rfind(".") != -1:
        last_slash = full_file_name.rfind(".")
        file_name = full_file_name[last_slash + 1 :]
        file_path = full_file_name[: last_slash + 1]
    else:
        raise Exception(f"INTERNAL ERROR - No slash in file name: {full_file_name}")
    return file_path, file_name



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
        '>' : symbols.GREATER,
        '>=' : symbols.GREATER_EQUAL,
        '<' : symbols.LESS,
        '<=' : symbols.LESS_EQUAL,
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
        'location' : symbols.LOCATION,
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