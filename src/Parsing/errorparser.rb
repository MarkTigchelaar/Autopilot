require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'


class ErrorParser
    def initialize()
        @keywords = getkeywords()
        @name = nil
        @itemList = Array.new()
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceError(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            errorNameStep(parser)
        else
            unexpectedToken(parser)
        end
        e = ErrorStatement.new(@name, @itemList)
        reset()
        return e
    end

    def errorNameStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IS)
            isStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def isStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            errorListItemStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def errorListItemStep(parser)
        token = parser.nextToken()
        @itemList.append(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def commaStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            errorListItemStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def reset()
        @name = nil
        @itemList = Array.new()
    end

    def enforceError(token)
        if(token.getText().upcase != ERROR)
            throw Exception.new("Did not enounter \"error\" keyword in file " + token.getFilename())
        end
    end

    def isEOF(token)
        return token.getType() == EOF
    end

    def addError(parser, message)
        #puts "ADDING ERROR"
         parser.addError(parser.nextToken(), message)
         parser.setToSync()
     end
 
     def eofReached(parser)
         msg = "End of file reached."
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
end

class ErrorStatement
    def initialize(name, itemList)
        @name = name
        @items = itemList
    end

    def _printLiteral()
        astString = ""
        astString += "(name: " + @name.getText() + ", items: ["
        for item in @items do
            astString += item.getText() + ", "
        end
        astString = astString[0...-2] + "])"
        return astString
    end
end