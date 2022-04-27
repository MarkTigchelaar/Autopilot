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

def invalidItemName(parser)
    msg = "Invalid name for item #{parser.peek().getText()}."
    addError(parser, msg)
end

def unexpectedToken(parser)
    msg = "Unexpected token #{parser.peek().getText()}."
    addError(parser, msg)
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

def addError(parser, message)
    parser.addError(parser.nextToken(), message)
    parser.setToSync()
end

def eofReached(parser)
    msg = "End of file reached."
    addError(parser, msg)
end

def emptyStatement(parser)
    msg = "Empty Statement."
    addError(parser, msg)
end

def noFunctions(parser)
    msg = "No functions defined."
    addError(parser, msg)
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

# Send statement parser into here to make it easier to maintain
# in one spot, instead of similar function here, and method in a different file.
def parse_internal_statement(statement_parser, main_parser)
    token = main_parser.peek()
    return case token.getType()
    when IF
        statement_parser.parseIf(main_parser)
    when ELIF
        statement_parser.parseElif(main_parser)
    when ELSE
        statement_parser.parseElse(main_parser)
    when UNLESS
        statement_parser.parseUnless(main_parser)
    when LOOP
        statement_parser.parseLoop(main_parser)
    when FOR
        statement_parser.parseFor(main_parser)
    when WHILE
        statement_parser.parseWhile(main_parser)
    when LET
        statement_parser.parseLet(main_parser)
    when VAR
        statement_parser.parseVar(main_parser)
    when BREAK
        statement_parser.parseBreak(main_parser)
    when CONTINUE
        statement_parser.parseContinue(main_parser)
    when RETURN
        statement_parser.parseReturn(main_parser)
    when SWITCH
        statement_parser.parseSwitch(main_parser)
    else
        nil
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