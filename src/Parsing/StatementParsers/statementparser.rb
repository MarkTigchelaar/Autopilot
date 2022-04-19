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
        reset()
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            #puts "parser sees: #{peekTok.getText()}"
            stmt = nil
            if(isValidIdentifier(peekTok))
                stmt = parseReassignOrCall(parser)
            else
                stmt = parse_internal_statement(self, parser)
            end
            #if(stmt != nil)
            @statements.append(stmt)
            peekTok = parser.peek()
            #else
            #    break
            #end
            #puts "Does parser have errors: #{parser.hasErrors()}"
            if(component_test and parser.hasErrors())
                #puts "breaking from loop in statement parser"
                break
            end
            #if(parser.hasErrors())
                #while(!isEOF(peekTok) and is_interal_statement_keyword(peekTok))
                    #parser.discard()
                #end
            #end
        end
        if(!component_test)
            if(isEOF(peekTok))
                #puts "End of file!"
                eofReached(parser)
            #elsif(peekTok.getType() == ENDSCOPE)
                #endStep(parser)
            #else
            #    #puts "UNEXPECTED TOKEN IN STATEMENT PARSER: #{peekTok.getText()}"
            #    unexpectedToken(parser)
            end
        end
        s = StatementList.new(@statements)
        reset()
        #puts "Does parser have errors at end of statement parse?: #{parser.hasErrors()}"
        #puts "returning statement from statement parser"
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
        #puts "PARSing assignment statement-------------------------------"
        a = @assignparser.parse(parser)
        #a.usesLet()
        return a
    end

    def parseVar(parser)
        a = @assignparser.parse(parser)
        #a.usesVar()
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