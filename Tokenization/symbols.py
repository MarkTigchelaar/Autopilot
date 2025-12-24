
# All recognized key words operators and symbols:
LEFT_PAREN = "LEFT_PAREN"
RIGHT_PAREN = "RIGHT_PAREN"
LEFT_BRACKET = "LEFT_BRACKET"
RIGHT_BRACKET = "RIGHT_BRACKET"
LEFT_BRACE = "LEFT_BRACE"
RIGHT_BRACE = "RIGHT_BRACE"

COMMA = "COMMA"
MINUS = "MINUS"
PLUS = "PLUS"
#SEMICOLON = "SEMICOLON"
COLON = "COLON"
SLASH = "SLASH"
STAR = "STAR"
CARROT = "CARROT"
MOD = "MOD" # %

# One or two character tokens.
#BANG = "BANG"
BANG_EQUAL = "BANG_EQUAL"
EQUAL = "EQUAL"
EQUAL_EQUAL = "EQUAL_EQUAL"
GREATER = "GREATER"
GREATER_EQUAL = "GREATER_EQUAL"
LESS = "LESS"
LESS_EQUAL = "LESS_EQUAL"

AND = "and".upper()
NAND = "nand".upper()
OR  = "or".upper()
XOR = "xor".upper()
NOR = "nor".upper()
NOT = "not".upper()


# combined assignment
PLUS_EQUAL = "PLUS_EQUAL"
MINUS_EQUAL = "MINUS_EQUAL"
STAR_EQUAL = "STAR_EQUAL"
SLASH_EQUAL = "SLASH_EQUAL"
CARROT_EQUAL = "CARROT_EQUAL"
MOD_EQUAL = "MOD_EQUAL"


# Literals.
IDENTIFIER = "IDENTIFIER"

# For user defined types, for type tokens
UNKNOWN_TYPE = "UNKNOWN_TYPE"


# Keywords.
LIBRARY = "library".upper()
MODULE = "module".upper()
IMPORT = "import".upper()
FROM = "from".upper()
LOCATION = "location".upper()
DEFINE = "define".upper()



FOR = "for".upper()
LOOP = "loop".upper()
WHILE = "while".upper()
CONTINUE = "continue".upper()
BREAK = "break".upper()

ERROR = "error".upper()

IF = "if".upper()
ELSE = "else".upper()
ELIF = "elif".upper()
UNLESS = "unless".upper()
SWITCH = "switch".upper()
CASE = "case".upper()
DEFAULT = "default".upper()


RETURN = "return".upper()

DO = "do".upper()
ENDSCOPE = "end".upper()

PUB = "pub".upper()
SELF = "self".upper()

FUN = "fun".upper()
#PRC = "prc".upper()
#LAMBDA  = "lambda".upper()
INLINE = "inline".upper()

INTERFACE = "interface".upper()
USES = "uses".upper()

ENUM = "enum".upper()
STRUCT = "struct".upper()
UNION = "union".upper()


# for defining data structures in "define" statements:

MAP = "Map".upper()
DICTIONARY = "Dictionary".upper()
HASHMAP = "HashMap".upper()

LIST = "List".upper()
LINKEDLIST = "LinkedList".upper()
VECTOR = "Vector".upper()

SET = "Set".upper()
HASHSET = "HashSet".upper()
TREESET = "TreeSet".upper()

STACK = "Stack".upper()

QUEUE = "Queue".upper()
FIFOQUEUE = "FifoQueue".upper()
PRIORITYQUEUE = "PriorityQueue".upper()
DEQUE = "Deque".upper()

OPTION = "Option".upper()
RESULT = "Result".upper()
NULL = "Null".upper()




ASSERT = "assert".upper()
DEBUG = "debug".upper()
UNITTEST = "unittest".upper()
DEFER = "defer".upper()

ACYCLIC = "acyclic".upper()
#UNIQUE = "unique".upper()

AS = "as".upper()
IS = "is".upper()
IN = "in".upper()



LET = "let".upper()
VAR = "var".upper()
INT = "int".upper()
LONG = "long".upper()
FLOAT = "float".upper()
DOUBLE = "double".upper()

CHAR = "char".upper()
STRING = "string".upper()

BOOL = "bool".upper()
TRUE = "true".upper()
FALSE = "false".upper()

RANGE = "RANGE" # ..
DOT = "DOT" # .

#YIELD = "yield".upper()
#SLEEP = "sleep".upper()
#TASKID = "tid".upper()

EOF = "EOF"
#ERROR = "ERROR"