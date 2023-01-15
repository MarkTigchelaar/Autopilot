require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/loop_statement.rb'

class LoopParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new
        @loop_name = nil
    end

    def parse(parser)
        errCount = parser.errorCount()
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
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
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
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmt = @statement_parser.parse(parser)
            @statements = stmt
            peekTok = parser.peek()
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
