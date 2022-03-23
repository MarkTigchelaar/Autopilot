
LEFT_PAREN = "LEFT_PAREN"
RIGHT_PAREN = "RIGHT_PAREN"
LEFT_BRACKET = "LEFT_BRACKET"
RIGHT_BRACKET = "RIGHT_BRACKET"
LEFT_BRACE = "LEFT_BRACE"
RIGHT_BRACE = "RIGHT_BRACE"
QUESTION = "QUESTION"
COMMA = "COMMA"
MINUS = "MINUS"
PLUS = "PLUS"
SEMICOLON = "SEMICOLON"
COLON = "COLON"
SLASH = "SLASH"
STAR = "STAR"
CARROT = "CARROT"
MOD = "MOD" # %

# One or two character tokens.
BANG = "BANG"
BANG_EQUAL = "BANG_EQUAL"
EQUAL = "EQUAL"
EQUAL_EQUAL = "EQUAL_EQUAL"
GREATER = "GREATER"
GREATER_EQUAL = "GREATER_EQUAL"
LESS = "LESS"
LESS_EQUAL = "LESS_EQUAL"

PLUS_EQUAL = "PLUS_EQUAL"
MINUS_EQUAL = "MINUS_EQUAL"
STAR_EQUAL = "STAR_EQUAL"
SLASH_EQUAL = "SLASH_EQUAL"
CARROT_EQUAL = "CARROT_EQUAL"
MOD_EQUAL = "MOD_EQUAL"

#HASH = "HASH"

# Literals.
IDENTIFIER = "IDENTIFIER"


# Keywords.
LIBRARY = "library".upcase
MODULE = "module".upcase
IMPORT = "import".upcase
#USE = "use".upcase
FROM = "from".upcase
#ALIAS = "alias".upcase
DEFINE = "define".upcase
FOR = "for".upcase
LOOP = "loop".upcase
WHILE = "while".upcase
CONTINUE = "continue".upcase
BREAK = "break".upcase
ERROR = "error".upcase


IF = "if".upcase
ELSE = "else".upcase
CASE = "case".upcase
SWITCH = "switch".upcase

RETURN = "return".upcase

DO = "do".upcase
ENDSCOPE = "end".upcase

PUB = "pub".upcase
SELF = "self".upcase

FUN = "fun".upcase
#PRC = "prc".upcase
LAMBDA  = "lambda".upcase
#CLASS = "class".upcase
#SUPER = "super".upcase
#INTERFACE = "interface".upcase
TRAIT = "trait".upcase
#ABSTRACT = "abstract".upcase
#EXTENDS = "extends".upcase
#IMPL = "impl".upcase
ENUM = "enum".upcase
STRUCT = "struct".upcase
UNION = "union".upcase

ASSERT = "assert".upcase
DEBUG = "debug".upcase
UNITTEST = "unittest".upcase
DEFER = "defer".upcase

ACYCLIC = "acyclic".upcase
UNIQUE = "unique".upcase

AS = "as".upcase
IS = "is".upcase
IN = "in".upcase

AND = "and".upcase
NAND = "nand".upcase
OR  = "or".upcase
XOR = "xor".upcase
NOR = "nor".upcase
NOT = "not".upcase

INT = "int".upcase
LONG = "long".upcase
FLOAT = "float".upcase
DOUBLE = "double".upcase

CHAR = "char".upcase
STRING = "string".upcase

BOOL = "bool".upcase
TRUE = "true".upcase
FALSE = "false".upcase

RANGE = "RANGE" # ..
DOT = "DOT" # .

YIELD = "yield".upcase
SLEEP = "sleep".upcase
TASKID = "tid".upcase
    
        # All 3 are concurrency related, but it just affects
        # current thread
/ implment threads and processes as classes instead. (for now)
SELECT = "select"
SEND = "send"
RECEIVE = "receive"



THREAD = "thread"
PROCESS = "process"
        
/

EOF = "EOF"