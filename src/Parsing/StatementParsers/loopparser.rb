require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class LoopParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceLoop(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            statementStep(parser)
        end
        l = LoopStatement.new(@statements)
        reset()
        return l
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
        @statements = Array.new
    end
end


class LoopStatement
    def initialize(sub_statements)
        @sub_statements = sub_statements
    end

    def _printLiteral
        l = Array.new
        for stmt in @sub_statements
            l.append(stmt._printLiteral())
        end
        return l.join("")
    end

    def _printTokType(type_list)
        for stmt in @sub_statements
            stmt._printTokType(type_list)
        end
    end
end