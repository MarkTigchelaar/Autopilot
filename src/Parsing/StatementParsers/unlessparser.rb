require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


class UnlessParser
    def initialize(expression_parser, statement_parser)
        @expression_parser = expression_parser
        @statement_parser = statement_parser
        @expression_ast = nil
        @statements = Array.new
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceUnless(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseExpression(parser)
        end
        i = UnlessStatement.new(@expression_ast, @statements)
        reset()
        return i  
    end
    
    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
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
            parseStatements(parser)
        end
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

    def enforceUnless(token)
        if(token.getText().upcase != UNLESS)
            throw Exception.new("Did not enounter \"unless\" keyword in file " + token.getFilename())
        end
    end
end


class UnlessStatement
    def initialize(expression_ast, statements)
        @expression_ast = expression_ast
        @statements = statements
    end
end