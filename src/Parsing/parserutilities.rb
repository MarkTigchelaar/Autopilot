
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
    if(@keywords.has_key?(token.getText()))
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

def isPrimitiveType(token)
    case token.getType()
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

def synchronize(parser)
    while(!parser.isAtEnd())
        literal = parser.peek().getType()
        if(literal == MODULE)
            return
        elsif(literal == FOR)
            return
        elsif(literal == LOOP)
            return
        elsif(literal == WHILE)
            return
        elsif(literal == CONTINUE)
            return
        elsif(literal == BREAK)
            return
        elsif(literal == IF)
            return
        elsif(literal == CASE)
            return
        elsif(literal == RETURN)
            return
        elsif(literal == PUB)
            return
        elsif(literal == FUN)
            return
        elsif(literal == PRC)
            return
        elsif(literal == LAMBDA)
            return
        elsif(literal == CLASS)
            return
        elsif(literal == INTERFACE)
            return
        elsif(literal == ABSTRACT)
            return
        elsif(literal == ENUM)
            return
        elsif(literal == ASSERT)
            return
        elsif(literal == DEBUG)
            return
        elsif(literal == ACYCLIC)
            return
        elsif(literal == INT)
            return
        elsif(literal == LONG)
            return
        elsif(literal == FLOAT)
            return
        elsif(literal == DOUBLE)
            return
        elsif(literal == CHAR)
            return
        elsif(literal == STRING)
            return
        elsif(literal == BOOL)
            return
        end
        parser.discard()
    end
end