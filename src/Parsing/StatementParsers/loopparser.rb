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
            puts "HERE"
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
            #if(parser.hasErrors())
            #    return
            #end
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@statements.length() == 0)
                emptyStatement(parser)
            else#if(not parser.hasErrors())
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

    def toJSON()
        return {
            "type" => "loop",
            "label" =>  @name != nil ? { "literal" => @name.getText(), "type" => @name.getType(), "line_number" => @name.getLine() } : nil,
            "statements" => @sub_statements.toJSON()
        }
    end

    def _printLiteral
        l = Array.new
        if(@name != nil)
            l.append(@name.getText())
        end
        l.append(@sub_statements._printLiteral())
        return l.join("")
    end

    def _printTokType(type_list)
        if(@name != nil)
            type_list.append(@name.getType())
        end
        @sub_statements._printTokType(type_list)
    end
end