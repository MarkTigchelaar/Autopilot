require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class SwitchParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @cases = Array.new
        @default_case = nil
        @test_case = nil
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        token = parser.nextToken()
        enforceSwitch(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            testExpStep(parser)
        else
            unexpectedToken(parser)
        end
        r = SwitchStatement.new(@test_case, @cases, @default_case)
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
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
        elsif(isOtherValidType(peekTok) and !isPrimitiveType(peekTok, true))
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
        elsif(peekTok.getType() == DO)
            doStep(parser, values)
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

    def doStep(parser, values)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
          parseStatements(parser, values)
        end  
    end

    def parseStatements(parser, values, from_default = false)
        peekTok = parser.peek()
        if(peekTok.getType() == DEFAULT and @default_case != nil)
            msg = "Invalid statement, switch statement allows exactly one default case."
            addError(parser, msg)
            return
        end
        statements = Array.new
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmts = @statement_parser.parse(parser)
            statements = stmts
            peekTok = parser.peek()
        end
        new_case = CaseStatement.new(values, statements)
        if(from_default)
            @default_case = new_case
        else
            @cases.append(new_case)
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == CASE and not from_default)
            if(statements.length() == 0)
                emptyStatement(parser)
            elsif(not parser.hasErrors())
                caseStep(parser)
            end
        elsif(peekTok.getType() == DEFAULT and not from_default)
            if(statements.length() == 0)
                emptyStatement(parser)
            else
                elseStep(parser)
            end
        elsif(peekTok.getType() == ENDSCOPE)
            if(statements.length() == 0)
                emptyStatement(parser)
            else
                endStep(parser)
            end
        else
            unexpectedToken(parser)
        end
    end

    def elseStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(!(is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            unexpectedToken(parser)
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
        @default_case = nil
    end
end

class CaseStatement
    def initialize(values, statements)
        @values = values
        @statements = statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        vals = Array.new()
        for v in @values
            vals.append({
                "literal" => v.getText(),
                "type" => v.getType(),
                "line_number" => v.getLine()
            })
        end
        stmts = @statements.toJSON()
        return {
            "values" => vals,
            "statements" => stmts
        }
    end

    def _printLiteral
        l = Array.new
        for val in @values
            l.append(val.getText() + ' ')
        end
        l.append(@statements._printLiteral() + ' ')
        return l.join("")
    end

    def _printTokType(type_list)
        for val in @values
            type_list.append(val.getType())
        end
        @statements._printTokType(type_list)
    end
end

class SwitchStatement
    def initialize(test_case, case_statements, default_case)
        @test_case = test_case
        @case_statements = case_statements
        @default_case = default_case
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "switch",
            "test_case" => {
                "literal" => @test_case.getText(),
                "type" => @test_case.getType(),
                "line_number" => @test_case.getLine()
            },
            "cases" => getCasesJSON()
        }
    end

    def getCasesJSON()
        cases = Array.new()
        for _case in @case_statements
            cases.append(_case.toJSON())
        end
        if(@default_case)
            cases.append(@default_case.toJSON())
        end
        return cases
    end

    def _printLiteral
        l = Array.new
        if(@test_case != nil)
            l.append(@test_case.getText() + ' ')
        end
        for stmt in @case_statements
            l.append(stmt._printLiteral())
        end
        if(@default_case != nil)
            l.append(@default_case._printLiteral())
        end
        str = l.join("").rstrip()
        return str
    end

    def _printTokType(type_list)
        if(@test_case != nil)
            type_list.append(@test_case.getType())
        end
        for stmt in @case_statements
            stmt._printTokType(type_list)
        end
        if(@default_case != nil)
            @default_case._printTokType(type_list)
        end
    end
end