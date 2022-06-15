require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'

class UnittestParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new()
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
        @statements = Array.new()
        @test_name = nil
    end
end

class UnittestStatement
    def initialize(name, statements)
        @test_name = name
        @statements = statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "unittest",
            "name" => {
                "literal" => @test_name.getText(),
                "type" => @test_name.getType(),
                "line_number" => @test_name.getLine()
            },
            "statements" => getStatements()
        }
    end

    def getStatements()
        @statements.toJSON()
    end

    def _printLiteral
        l = Array.new
        if(@test_name != nil)
            l.append(@test_name.getText() + ' ')
        end
        l.append(@statements._printLiteral())
        return l.join("").rstrip()
    end

    def _printTokType(type_list)
        if(@test_name != nil)
            type_list.append(@test_name.getType())
        end
        @statements._printTokType(type_list)
    end
end
