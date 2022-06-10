require_relative '../keywords.rb'

def isIdentifier(token)
    specialIdChars = ["@", "$", "_" , "~", "#", "&", ";"]
    if(isAlphaNumericWord(token))
        return true
    end
    if(specialIdChars.include?(token.getText()[0]))
        return true
    end
    return false
end

def isAlphaNumericWord(token)
    literal = token.getText()
    if(!isAlpha(literal[0]))
        return false
    end
    l = literal[1 .. literal.length]
    for i in 1 .. l.length - 1 do
        if(!isAlphaNumeric(l[i]))
            return false
        end
    end
    return true
end

def isNumeric(token)
    literal = token.getText()
    if(!isDigit(literal[0]))
        return false
    end
    for i in 0 .. literal.length - 1 do
        if(!isDigit(literal[i]) and literal[i] != '_')
            return false
        end
    end
    return true
end

def isInt(token)
    tokliteral = token.getText()
    for i in 0 .. tokliteral.length-1 do
        if(!isDigit(tokliteral[i]))
            return false
        end
    end
    return true
end

def isFloat(token)
    tokliteral = token.getText()
    decimal = 0
    for i in 0 .. tokliteral.length-1 do
        if(!isDigit(tokliteral[i]) and tokliteral[i] != '.')
            return false
        end
        if(tokliteral[i] == '.')
            decimal += 1
        end
    end
    if(decimal > 1)
        return false
    end
    return true
end

def is_string_or_char(token)
    return true if token.getType() == STRING
    return true if token.getType() == CHAR
    return false
end

# Utility functions
def isDigit(char)
    return ((char >= "0") and (char <= "9"))
end

def isAlpha(char)
    islowercase = (char.ord >= 'a'.ord && char.ord <= 'z'.ord)
    isuppercase = (char.ord >= 'A'.ord && char.ord <= 'Z'.ord)
    return (islowercase or isuppercase or char == '_')
end

def isAlphaNumeric(char)
    return (isAlpha(char) or isDigit(char))
end

def isForbiddenInExpressions(token)
    if(isEOF(token))
        return true
    elsif(isScopeKeyword(token))
        return true
    elsif(isGeneralKeyWord(token.getText()))
        return true
    end
    return false
end
    
def is_valid_r_value_keyword(token)
    case token.getType()
    when TRUE
        true
    when FALSE
        false
    end
end

def isOperator(token)
    case token.getType()
        when PLUS
            true
        when MINUS
            true
        when COLON
            true
        when SLASH
            true
        when STAR
            true
        when CARROT
            true
        when MOD
            true
        when BANG_EQUAL
            true
        when EQUAL_EQUAL
            true
        when GREATER
            true
        when GREATER_EQUAL
            true
        when LESS
            true
        when LESS_EQUAL
            true
        when AND
            true
        when NAND
            true
        when OR
            true
        when XOR
            true
        when NOR
            true
        when NOT
            true
        else
            false
        end
end

def invalidItemName(parser)
    msg = "Invalid name for item #{parser.peek().getText()}."
    ERRORS::addError(parser, msg)
end

def unexpectedToken(parser)
    msg = "Unexpected token #{parser.peek().getText()}."
    ERRORS::addError(parser, msg)
end

def isEOF(token)
    return token.getType() == EOF
end

def isValidIdentifier(token)
    if(isKeyword(token))
        return false
    end
    return isIdentifier(token)
end

def isKeyword(token)
    keywords = getkeywords()
    if(keywords.has_key?(token.getText()))
        return true
    end
    return false
end

# rant
    # Yes, this mini module is a hack:
    # Used to get around a name collision bug, where the expression parser
    # method of the same name gets called from eofReached (below) ... because Ruby.
    # I don't care if there is a explaination as to why, it's either a bug in the language,
    # Or some code ninja is on Rubys design team.
    # Thank the software gods for the idea of automated integration (regression) tests.
# end
module ERRORS
def self.addError(parser, message)
    tok = parser.nextToken()
    parser.addError(tok, message)
    parser.setToSync()
end
end

def eofReached(parser)
    msg = "End of file reached."
    ERRORS::addError(parser, msg)
end

def emptyStatement(parser)
    msg = "Empty Statement."
    ERRORS::addError(parser, msg)
end

def noFunctions(parser)
    msg = "No functions defined."
    ERRORS::addError(parser, msg)
end

def isPrimitiveType(token, check_literal = false)
    compare = token.getType()
    if(check_literal)
        compare = token.getText().upcase
    end
    case compare
        when INT
            return true
        when LONG
            return true
        when FLOAT
            return true
        when DOUBLE
            return true
        when CHAR
            return true
        when STRING
            return true
        when BOOL
            return true
        else
            return false
    end
end

def isOtherValidType(peekTok)
    case peekTok.getType()
    when INT
        true
    when LONG
        true
    when FLOAT
        true
    when DOUBLE
        true
    when CHAR
        true
    when STRING
        true
    when BOOL
        true
    else
        false
    end
end


def isScopeKeyword(token)
    token.getType() == DO
end

def is_interal_statement_keyword(token)
    return case token.getType()
    when IF
        true
    when ELIF
        true
    when ELSE
        true
    when UNLESS
        true
    when LOOP
        true
    when FOR
        true
    when WHILE
        true
    when LET
        true
    when VAR
        true
    when BREAK
        true
    when CONTINUE
        true
    when RETURN
        true
    when SWITCH
        true
    else
        false
    end
end

def internalSynchronize(parser)
    peekTok = parser.peek()
    while(!isEOF(peekTok) and (peekTok.getType() != ENDSCOPE) and !is_interal_statement_keyword(peekTok))
        parser.discard()
        peekTok = parser.peek()
    end
end


def isExternalKeyword(token)
    return case token.getType()
    when MODULE
        true
    when IMPORT
        true
    when DEFINE
        true
    when UNITTEST
        true
    when FUN
        true
    when INTERFACE
        true
    when ENUM
        true
    when ACYCLIC
        true
    when UNION
        true
    when ERROR
        true
    when STRUCT
        true
    else
        false
    end
end

def externalSynchronize(parser)
    token = parser.peek()
    while(!parser.isAtEnd() and !isExternalKeyword(token))
        parser.discard()
        token = parser.peek()
    end
end

def isGeneralKeyWord(tok_literal)
    case tok_literal.upcase
    when LIBRARY
        true
    when MODULE
        true
    when IMPORT
        true
    when FROM
        true
    when DEFINE
        true
    when FOR
        true
    when LOOP
        true
    when WHILE
        true
    when CONTINUE
        true
    when BREAK
        true
    when IF
        true
    when ELSE
        true
    when ELIF
        true
    when UNLESS
        true
    when CASE
        true
    when DEFAULT
        true
    when SWITCH
        true
    when RETURN
        true
    when DO
        true
    when ENDSCOPE
        true
    when PUB
        true
    when SELF
        true
    when FUN
        true
    when LAMBDA
        true
    when INLINE
        true
    when STRUCT
        true
    when INTERFACE
        true
    when USES
        true
    when ERROR
        true
    when UNION
        true
    when ENUM
        true
    when ASSERT
        true
    when DEBUG
        true
    when UNITTEST
        true
    when DEFER
        true
    when ACYCLIC
        true
    when UNIQUE
        true
    when AS
        true
    when IS
        true
    when IN
        true
    when AND
        true
    when NAND
        true
    when OR
        true
    when XOR
        true
    when NOR
        true
    when NOT
        true
    when VAR
        true
    when LET
        true
    when INT
        true
    when LONG
        true
    when FLOAT
        true
    when DOUBLE
        true
    when CHAR
        true
    when STRING
        true
    when BOOL
        true
    when TRUE
        true
    when FALSE
        true
    when DOT
        true
    when RANGE
        true
    when LEFT_PAREN
        true
    when RIGHT_PAREN
        true
    when COMMA
        true
    when EOF
        true
    else
        false
    end
end