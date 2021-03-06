require './tokentype.rb'

# Change to a case statement, and return bool
def getkeywords
    keywords = {
        "library" => LIBRARY,
        "module" => MODULE,
        "import" => IMPORT,
        "from" => FROM,
        "define" => DEFINE,
        "for" => FOR,
        "loop" => LOOP,
        "while" => WHILE,
        "continue" => CONTINUE,
        "break" => BREAK,
        "if" => IF,
        "else" => ELSE,
        "elif" => ELIF,
        "unless" => UNLESS,
        "case" => CASE,
        "default" => DEFAULT,
        "switch" => SWITCH,
        "return" => RETURN,
        "do" => DO,
        "end" => ENDSCOPE,
        "pub" => PUB,
        "self" => SELF,
        "fun" => FUN,
        "lambda" => LAMBDA,
        "inline" => INLINE,
        "struct" => STRUCT,
        "interface" => INTERFACE,
        "uses" => USES, 
        "error" => ERROR,
        "union" => UNION,
        "enum" => ENUM,
        "assert" => ASSERT,
        "debug" => DEBUG,
        "unittest" => UNITTEST,
        "defer" => DEFER,
        "acyclic" => ACYCLIC,
        "unique" => UNIQUE,
        "as" => AS,
        "is" => IS,
        "in" => IN,
        "and" => AND,
        "nand" => NAND,
        "or" => OR,
        "xor" => XOR,
        "nor" => NOR,
        "not" => NOT,
        "var" => VAR,
        "let" => LET,
        "int" => INT,
        "long" => LONG,
        "float" => FLOAT,
        "double" => DOUBLE,
        "char" => CHAR,
        "string" => STRING,
        "bool" => BOOL,
        "true" => TRUE,
        "false" => FALSE,
        "." => DOT,
        ".." => RANGE,
        "(" => LEFT_PAREN,
        ")" => RIGHT_PAREN,
        "," => COMMA,
        "yield" => YIELD,
        "sleep" => SLEEP,
        "tid" => TASKID,
        "EOF" => EOF
    }
    return keywords
end