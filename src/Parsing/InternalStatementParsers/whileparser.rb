require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/while_statement.rb'

class WhileParser
    def initialize(expression_parser, statement_parser)
        @expression_parser = expression_parser
        @statement_parser = statement_parser
        @expression_ast = nil
        @loop_name = nil
        @statements = Array.new
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        token = parser.nextToken()
        enforceWhile(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or is_boolean_keyword(peekTok))
            parseExpression(parser)
        else
            unexpectedToken(parser)
        end
        w = WhileStatement.new(@loop_name, @expression_ast, @statements)
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        return w
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            unexpectedToken(parser)
        end
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
            parseStatements(parser)
        end
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmts = @statement_parser.parse(parser)
            @statements = stmts
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
    
    def reset()
        @loop_name = nil
        @expression_ast = nil
        @statements = Array.new
    end

    def enforceWhile(token)
        if(token.getType() != WHILE)
            throw Exception.new("Did not enounter \"while\" keyword in file " + token.getFilename())
        end
    end
end
