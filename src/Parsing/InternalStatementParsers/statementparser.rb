require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


require './Parsing/InternalStatementParsers/returnparser.rb'
require './Parsing/InternalStatementParsers/continueparser.rb'
require './Parsing/InternalStatementParsers/breakparser.rb'
require './Parsing/InternalStatementParsers/loopparser.rb'
require './Parsing/InternalStatementParsers/switchparser.rb'
require './Parsing/InternalStatementParsers/ifparser.rb'
require './Parsing/InternalStatementParsers/elseparser.rb'
require './Parsing/InternalStatementParsers/elifparser.rb'
require './Parsing/InternalStatementParsers/unlessparser.rb'
require './Parsing/InternalStatementParsers/assignparser.rb'
require './Parsing/InternalStatementParsers/whileparser.rb'
require './Parsing/InternalStatementParsers/forparser.rb'
require './Parsing/InternalStatementParsers/reassignorcallparser.rb'

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

    def parse(parser, component_test = false, in_if = false)
        stmts = Array.new
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            # add function here for when inside if/elif statement check for elif / else, break if found
            stmt = nil
            if(isValidIdentifier(peekTok))
                stmt = parseReassignOrCall(parser)
            else
                
                stmt = case peekTok.getType()
                when IF
                    parseIf(parser)
                when ELIF
                    if(in_if and prev_not_elif_or_if(stmts))
                        break
                    end
                    parseElif(parser)
                when ELSE
                    if(in_if and prev_not_elif_or_if(stmts))
                        break
                    end
                    parseElse(parser)
                when UNLESS
                    parseUnless(parser)
                when LOOP
                    parseLoop(parser)
                when FOR
                    parseFor(parser)
                when WHILE
                    parseWhile(parser)
                when LET
                    parseLet(parser)
                when VAR
                    parseVar(parser)
                when BREAK
                    parseBreak(parser)
                when CONTINUE
                    parseContinue(parser)
                when RETURN
                    parseReturn(parser)
                when SWITCH
                    parseSwitch(parser)
                else
                    nil
                end
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

    def prev_not_elif_or_if(stmts)
        return !["IfStatement", "ElifStatement"].include?(stmts[-1].class.name.split('::').last)
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

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def length()
        return @statements.length()
    end

    def toJSON()
        stmts = Array.new()
        for s in @statements
            stmts.append(s.toJSON())
        end
        return stmts
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