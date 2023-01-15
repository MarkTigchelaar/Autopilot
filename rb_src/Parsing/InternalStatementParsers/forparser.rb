require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/for_statement.rb'

class ForParser
    def initialize(expression_parser, statement_parser)
        @expression_parser = expression_parser
        @statement_parser = statement_parser
        @loop_name = nil
        @start_collection_ast = nil
        @stop_collection_ast = nil
        @let = false
        @var = false
        @opt_variable = nil
        @var_one = nil
        @var_two = nil
        @statements = Array.new
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        token = parser.nextToken()
        enforceFor(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LET)
            letStep(parser)
        elsif(peekTok.getType() == VAR)
            varStep(parser)    
        elsif(isValidIdentifier(peekTok) or isInt(peekTok))
            varOneStep(parser)
        else
            unexpectedToken(parser)
        end
        f = ForStatement.new(
            @loop_name,
            @let, 
            @var,
            @var_one,
            @var_two,
            @opt_variable, 
            @start_collection_ast, 
            @stop_collection_ast, 
            @statements
        )
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        return f
    end

    def letStep(parser)
        parser.discard()
        peekTok = parser.peek()
        @let = true
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            opt_variableDeclareStep(parser)
        else
            unexpectedToken(parser)
        end    
    end

    def varStep(parser)
        parser.discard()
        peekTok = parser.peek()
        @var = true
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            opt_variableDeclareStep(parser)
        else
            unexpectedToken(parser)
        end 
    end

    def opt_variableDeclareStep(parser)
        @opt_variable = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IN)
            inStep(parser, true)
        else
            unexpectedToken(parser)
        end
    end

    def varOneStep(parser)
        @var_one = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IN)
            inStep(parser, false)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def commaStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            varTwoStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def varTwoStep(parser)
        @var_two = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IN)
            inStep(parser, false)
        else
            unexpectedToken(parser)
        end
    end

    def inStep(parser, option_or_var_path = false)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isInt(peekTok))
            if(option_or_var_path)
                stopCollectionStep(parser)
            else
                startCollectionStep(parser)
            end
        else
            unexpectedToken(parser)
        end
    end

    def startCollectionStep(parser)
        @expression_parser.loadTokenizer(parser)
        @start_collection_ast = @expression_parser.parse_expression()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RANGE)
            rangeStep(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def rangeStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isInt(peekTok))
            stopCollectionStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def stopCollectionStep(parser)
        @expression_parser.loadTokenizer(parser)
        @stop_collection_ast = @expression_parser.parse_expression()
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
        if(!isEOF(peekTok) and is_interal_statement_keyword(peekTok))
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
        @start_collection_ast = nil
        @stop_collection_ast = nil
        @let = false
        @var = false
        @var_one = nil
        @var_two = nil
        @opt_variable = nil
        @statements = Array.new
    end

    def enforceFor(token)
        if(token.getType() != FOR)
            throw Exception.new("Did not enounter \"for\" keyword in file " + token.getFilename())
        end
    end
end
