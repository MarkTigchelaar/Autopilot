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
        reset()
        token = parser.nextToken()
        enforceSwitch(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            testExpStep(parser)
        #elsif(isOtherValidType(peekTok))
            #testExpStep(parser)
        else
            unexpectedToken(parser)
        end
        r = SwitchStatement.new(@test_case, @cases, @default_case)
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
        #elsif(is_interal_statement_keyword(peekTok))
        elsif(peekTok.getType() == DO)
            #parseStatements(parser, values)
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
        #elsif(is_interal_statement_keyword(peekTok))
        else
          parseStatements(parser, values)
        #else
        #    unexpectedToken(parser)
        end  
    end

    def parseStatements(parser, values, from_default = false)
        peekTok = parser.peek()
        puts "statement name: #{peekTok.getText()}, from fdefault: #{from_default}"
        if(peekTok.getType() == DEFAULT and @default_case != nil)
            msg = "Invalid statement, switch statement allows exactly one default case."
            addError(parser, msg)
            return
        end
        statements = Array.new
        while(!isEOF(peekTok) and is_interal_statement_keyword(peekTok))
            stmt = @statement_parser.parse(parser)
            statements.append(stmt)
            peekTok = parser.peek()
            if(parser.hasErrors())
                puts "HAS errors!!"
                return
            end
        end
        new_case = CaseStatement.new(values, statements)
        if(from_default)
            puts "default"
            @default_case = new_case
        else
            puts "regular case"
            @cases.append(new_case)
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == CASE and not from_default)
            puts "In parse statements, found case statement, not from default"
            if(statements.length() == 0)
                emptyStatement(parser)
            else
                caseStep(parser)
            end
        elsif(peekTok.getType() == DEFAULT and not from_default)
            puts "found default"
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
        elsif(!is_interal_statement_keyword(peekTok))#.getType() == ENDSCOPE)
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

    def _printLiteral
        l = Array.new
        #if(@test_case != nil)
        #    l.append(@test_case)
        #end
        for val in @values
            puts "in case, printing literal: #{val.getText()}"
            l.append(val.getText() + ' ')
        end
        for stmt in @statements
            puts "in statements, printing literal: #{stmt._printLiteral()}"
            l.append(stmt._printLiteral() + ' ')
        end
        return l.join("")
    end

    def _printTokType(type_list)
        for val in @values
            type_list.append(val.getType())
        end
        for stmt in @statements
            stmt._printTokType(type_list)
        end
    end
end

class SwitchStatement
    def initialize(test_case, case_statements, default_case)
        #if(test_case != nil)
        #  puts "Test case: #{test_case.getText()}, type: #{test_case.getType()}"
        #end
        #for c in case_statements
        #    puts "case value: #{c.getText()}, type: #{c.getType()}"
        #end
        if(default_case != nil)
            puts "Test case: #{default_case._printLiteral()}"
        end
        @test_case = test_case
        @case_statements = case_statements
        @default_case = default_case
    end

    def _printLiteral
        #puts "print literal for switch------"
        l = Array.new
        if(@test_case != nil)
            l.append(@test_case.getText() + ' ')
        end
        for stmt in @case_statements
            puts "------------------from statement"
            l.append(stmt._printLiteral())
        end
        if(@default_case != nil)
            puts "----------------from default"
            l.append(@default_case._printLiteral())
        end
        str = l.join("").rstrip()
        puts "result string: #{str}"
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