require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


class StatementParser
    def initialize(expression_parser)
        @expression_parser = expression_parser

        @assignparser = AssignParser.new(expression_parser)
        @reassignorcallparser = ReassignOrCallParser.new(expression_parser)

        @ifparser = IfParser.new(expression_parser, self)
        @elifparser = ElifParser.new(@ifparser)
        @unlessparser = UnlessParser.new(expression_parser, self)
        @elseparser = ElseParser.new(self)
        @switchparser = SwitchParser.new(self)
        
        @forparser = ForParser.new(expression_parser, self)
        @whileparser = WhileParser.new(expression_parser, self)
        @loopparser = LoopParser.new(self)

        @breakparser = BreakParser.new()
        @continueparser = ContinueParser.new()

        @returnparser = ReturnParser.new(expression_parser)
        
        @statements = statements
    end

    def parse(parser)
        reset()
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmt = nil
            if(isValidIdentifier(peekTok))
                stmt = parseReassignOrCall(parser)
            else
                stmt = parse_internal_statement(self, parser)
            end
            if(stmt != nil)
                @statements.append(stmt)
                peekTok = parser.peek()
            else
                break
            end
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
        s = StatementList.new(@statements)
        reset()
        return s
    end

    def parseIf(parser)
        @ifparser.parse(parser)
    end

    def parseElif(parser)
        @ElifParser.parse(parser)
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

    def parseLet(parser)
        a = @assignparser.parse(parser)
        a.usesLet()
        return a
    end

    def parseVar(parser)
        a = @assignparser.parse(parser)
        a.usesVar()
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

    def endStep(parser)
        parser.discard()
    end

    def reset()
        @statements = Array.new
    end
end

class StatementList
    def initialize(statements)
        @statements = statements
    end
end