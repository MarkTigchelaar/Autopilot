require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'

class UnittestParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new()
        @test_name = nil
        @keywords = getkeywords()
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceUnittest(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            testNameStep(parser)
        else
            unexpectedToken(parser)
        end
        u = UnittestStatement.new(@test_name, @statements)
        reset()
        return u
    end

    def testNameStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def doStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isKeyword(peekTok) and peekTok.getType() != ENDSCOPE)
            parseStatements(parser)
        else
            unexpectedToken(parser)
        end
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        while(!isEOF(peekTok) and peekTok.getType() != ENDSCOPE)
            @statements.append(@statement_parser.parse(parser))
        end
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def enforceUnittest(token)
        if(token.getText().upcase != UNITTEST)
            throw Exception.new("Did not enounter \"unittest\" keyword in file " + token.getFilename())
        end
    end

    def reset()
        @statements = Array.new()
        @test_name = nil
    end
end

class UnittestStatement
    def initialize(name, statements)
        @test_name = name
        @statements = statements
    end
end
