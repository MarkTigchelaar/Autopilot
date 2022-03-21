require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'


class DefineParser

    def initialize()
        @keywords = getkeywords()
        @oldNameToken = nil
        @newNameToken = nil
    end


    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceDefine(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            oldNameStep(parser)
        else
            invalidItemName(parser)
        end
        return defineStatement()
    end

    def oldNameStep(parser)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        end
        @oldNameToken = peekTok
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def asStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            newNameStep(parser)
        else
            invalidItemName(parser)
        end
    end

    def newNameStep(parser)
        name = parser.nextToken()
        if(!isValidIdentifier(name))
            invalidItemName(parser)
        else
            @newNameToken = name
        end
    end

    def defineStatement()
        result = DefineStatement.new(@oldNameToken, @newNameToken)
        reset()
        return result
    end

    def enforceDefine(peekTok)
        if(peekTok.getText().upcase != DEFINE)
            throw Exception.new("Did not enounter \"define\" keyword in file " + peekTok.getFilename())
        end
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
        reset()
    end

    def eofReached(parser)
        msg = "End of file reached."
        addError(parser, msg)
    end
    
    def reset()
        @oldNameToken = nil
        @newNameToken = nil
    end
end


class DefineStatement
    def initialize(oldName, newName)
        @oldNameToken = oldName
        @newNameToken = newName
    end

    def _printLiteral
        return "old name: #{@oldNameToken.getText()} new name: #{@newNameToken.getText()}"
    end
end