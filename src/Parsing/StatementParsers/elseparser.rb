require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative './ifparser.rb'

class ElseParser
    def initialize(expression_parser, statement_parser, ifparser)
        @ifparser = ifparser
        @expression_parser = expression_parser
        @statement_parser = statement_parser
        @statements = Array.new
        @if_statement = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceElse(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IF)
            @if_statement = @ifparser.parse(parser)
        elsif(is_interal_statement_keyword(peekTok))
            parseStatements(parser)
        else
            unexpectedToken(parser)
        end
        e = ElseStatement.new(@if_statement, @statements)
        reset()
        return e
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        while(!isEOF(peekTok) and is_interal_statement_keyword(peekTok))
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
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def reset()
        @expression_ast = nil
        @statements = Array.new
    end

    def enforceElse(token)
        if(token.getText().upcase != ELSE)
            throw Exception.new("Did not enounter \"else\" keyword in file " + token.getFilename())
        end
    end

end

class ElseStatement
    def initialize(if_statement, sub_statements)
        @if_statement = if_statement
        @sub_statements = sub_statements
    end
end