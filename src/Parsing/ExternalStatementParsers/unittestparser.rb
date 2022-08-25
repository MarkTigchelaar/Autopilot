require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/unittest_statement.rb'

class UnittestParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = nil
        @test_name = nil
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
        @test_name = parser.nextToken()
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
        else
          parseStatements(parser)
        end
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            @statements = @statement_parser.parse(parser)
            peekTok = parser.peek()
            if(parser.hasErrors())
                return
            end
        end
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@statements.length() == 0)
                emptyStatement(parser)
            else
                endStep(parser)
            end
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
        @statements = nil
        @test_name = nil
    end
end
