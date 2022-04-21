require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class StatementParser
    def initialize(expression_parser, dummy = nil)
        if(dummy != nil)
            sub_stmt_parser = dummy
        else
            sub_stmt_parser = self
        end
        @expression_parser = expression_parser

        @assignparser = AssignParser.new(expression_parser)
        @reassignorcallparser = ReassignOrCallParser.new(expression_parser)

        @ifparser = IfParser.new(expression_parser, sub_stmt_parser)
        @elifparser = ElifParser.new(@ifparser)
        @unlessparser = UnlessParser.new(@ifparser)
        @elseparser = ElseParser.new(sub_stmt_parser)
        @switchparser = SwitchParser.new(sub_stmt_parser)
        
        @forparser = ForParser.new(expression_parser, sub_stmt_parser)
        @whileparser = WhileParser.new(expression_parser, sub_stmt_parser)
        @loopparser = LoopParser.new(sub_stmt_parser)

        @breakparser = BreakParser.new()
        @continueparser = ContinueParser.new()

        @returnparser = ReturnParser.new(expression_parser)
        
        @statements = Array.new
    end

    def parse(parser, component_test = false)
        stmts = Array.new
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmt = nil
            errCount = parser.errorCount()
            if(isValidIdentifier(peekTok))
                stmt = parseReassignOrCall(parser)
            else
                stmt = parse_internal_statement(self, parser)
            end
            stmts.append(stmt)
            peekTok = parser.peek()
            if(component_test and parser.hasErrors())
                break
            end
        end
        s = StatementList.new(stmts)
        return s
    end

    def parseIf(parser)
        @ifparser.parse(parser)
    end

    def parseElif(parser)
        @elifparser.parse(parser)
    end

    def parseElse(parser)
        @elseparser.parse(parser)
    end

    def parseUnless(parser)
        @unlessparser.parse(parser)
    end

    def parseLoop(parser)
        @loopparser.parse(parser)
    end

    def parseWhile(parser)
        @whileparser.parse(parser)
    end

    def parseFor(parser)
        @forparser.parse(parser)
    end

    def parseLet(parser)
        a = @assignparser.parse(parser)
        return a
    end

    def parseVar(parser)
        a = @assignparser.parse(parser)
        return a
    end

    def parseBreak(parser)
        @breakparser.parse(parser)
    end

    def parseContinue(parser)
        @continueparser.parse(parser)
    end

    def parseReturn(parser)
        @returnparser.parse(parser)
    end

    def parseSwitch(parser)
        @switchparser.parse(parser)
    end

    def parseReassignOrCall(parser)
        @reassignorcallparser.parse(parser)
    end
end







class StatementList
    def initialize(statements)
        @statements = statements
    end

    def length()
        return @statements.length()
    end

    def _printLiteral
        lit = ""
        for stmt in @statements
            lit += stmt._printLiteral()
        end
        return lit
    end

    def _printTokType(type_list)
        for stmt in @statements
            stmt._printTokType(type_list)
        end
    end
end