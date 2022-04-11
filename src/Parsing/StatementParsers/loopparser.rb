require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class LoopParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new
        @loop_name = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceLoop(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        else
            statementStep(parser)
        end
        l = LoopStatement.new(@loop_name, @statements)
        reset()
        return l
    end

    def asStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            loopNameStep(parser)
        else
            unexpectedToken(parser)
        end 
    end

    def loopNameStep(parser)
        @loop_name = parser.nextToken()
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
            statementStep(parser)
        end
    end

    def statementStep(parser)
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmt = @statement_parser.parse(parser)
            @statements.append(stmt)
            peekTok = parser.peek()
            if(parser.hasErrors())
                return
            end
        end
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

    def enforceLoop(token)
        if(token.getText().upcase != LOOP)
            throw Exception.new("Did not enounter \"loop\" keyword in file " + token.getFilename())
        end
    end

    def reset()
        @loop_name = nil
        @statements = Array.new
    end
end


class LoopStatement
    def initialize(name, sub_statements)
        @name = name
        @sub_statements = sub_statements
    end

    def _printLiteral
        l = Array.new
        if(@name != nil)
            l.append(@name.getText())
        end
        for stmt in @sub_statements
            l.append(stmt._printLiteral())
        end
        return l.join("")
    end

    def _printTokType(type_list)
        if(@name != nil)
            type_list.append(@name.getType())
        end
        for stmt in @sub_statements
            stmt._printTokType(type_list)
        end
    end
end