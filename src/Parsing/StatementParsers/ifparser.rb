require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


class IfParser
    def initialize(expression_parser, statement_parser)
        @expression_parser = expression_parser
        @statement_parser = statement_parser
        @expression_ast = nil
        @statements = Array.new
        @let = false
        @var = false
        @opt_variable = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceIf(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LET)
            letStep(parser)
        elsif(peekTok.getType() == VAR)
            varStep(parser)
        else
            parseExpression(parser)
        end
        i = IfStatement.new(@let, @var, @expression_ast, @statements)
        reset()
        return i  
    end
    
    def letStep(parser)
        @let = true
        preOptStep(parser)
    end

    def varStep(parser)
        @var = true
        preOptStep(parser)
    end

    def preOptStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            optionUnwrappedVarStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def optionUnwrappedVarStep(parser)
        token = parser.nextToken()
        @opt_variable = token
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == EQUAL_EQUAL)
            equalStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def equalStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            optionNameStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def optionNameStep(parser)
        parser.discard()
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
            parseStatements(parser)
        end
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            unexpectedToken(parser)
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
        @let = false
        @var = false
        @opt_variable = nil
    end

    def enforceIf(token)
        if(token.getText().upcase != IF)
            throw Exception.new("Did not enounter \"if\" keyword in file " + token.getFilename())
        end
    end
end


class IfStatement
    def initialize(let, var, expression_ast, statements)
        @let = let
        @var = var
        @expression_ast = expression_ast
        @statements = statements
    end
end