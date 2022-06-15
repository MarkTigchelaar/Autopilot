require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/error_statement.rb'

class ErrorParser
    def initialize()
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
        @name = parser.nextToken()
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
end
