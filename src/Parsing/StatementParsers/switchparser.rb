require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class SwitchParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @cases = Array.new
        @else_case = nil
        @test_case = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceSwitch(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            testExpStep(parser)
        elsif(isOtherValidType(peekTok))
            testExpStep(parser)
        else
            unexpectedToken(parser)
        end
        r = SwitchStatement.new(@test_case, @cases, @else_case)
        reset()
        return r
    end

    def testExpStep(parser)
        current = parser.nextToken()
        @test_case = current
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == CASE)
            caseStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def caseStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            values = Array.new
            caseValueStep(parser, values)
        elsif(isOtherValidType(peekTok))
            values = Array.new
            caseValueStep(parser, values)
        else
            unexpectedToken(parser)
        end
    end

    def caseValueStep(parser, values)
        value = parser.nextToken()
        values.append(value)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser, values)
        elsif(is_interal_statement_keyword(peekTok))
            parseStatements(parser, values)
        else
            unexpectedToken(parser)
        end
    end

    def commaStep(parser, values)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            caseValueStep(parser, values)
        elsif(isOtherValidType(peekTok))
            caseValueStep(parser, values)
        else
            unexpectedToken(parser)
        end
    end

    def parseStatements(parser, values, from_else = false)
        peekTok = parser.peek()
        statements = Array.new
        while(!isEOF(peekTok) and is_interal_statement_keyword(peekTok))
            stmt = @statement_parser.parse(parser)
            statements.append(stmt)
            peekTok = parser.peek()
            if(parser.hasErrors())
                return
            end
        end
        new_case = CaseStatement.new(values, statements)
        if(from_else)
            @else_case = new_case
        else
            @cases.append(new_case)
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == CASE and not from_else)
            caseStep(parser)
        elsif(peekTok.getType() == ELSE and not from_else)
            elseStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def elseStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseStatements(parser, Array.new, true)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def enforceSwitch(token)
        if(token.getText().upcase != SWITCH)
            throw Exception.new("Did not enounter \"switch\" keyword in file " + token.getFilename())
        end
    end

    def reset()
        @return_expression = nil
        @test_case = nil
        @cases = Array.new
    end
end

class CaseStatement
    def initialize(values, statements)
        @values = values
        @statements = statements
    end
end

class SwitchStatement
    def initialize(test_case, case_statements, else_case)
        @test_case = test_case
        @case_statements = case_statements
        @else_case = else_case
    end
end