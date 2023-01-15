require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/if_statement.rb'

class IfParser
    def initialize(expression_parser, statement_parser)
        @expression_parser = expression_parser
        @statement_parser = statement_parser

        @expression_ast = nil
        @statements = Array.new
        @let = false
        @var = false
        @unwrapped_var = nil
        @opt_variable = nil

        @ifstatement = nil

        @is_unless = false
    end

    def is_unless()
        @is_unless = true
    end

    def isnt_unless()
        @is_unless = false
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        @ifstatement = IfStatement.new()
        token = parser.nextToken()
        enforceIf(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LET)
            if(@is_unless)
                unexpectedToken(parser)
                return
            end
            letStep(parser)
        elsif(peekTok.getType() == VAR)
            if(@is_unless)
                unexpectedToken(parser)
                return
            end
            varStep(parser)
        elsif(isValidIdentifier(peekTok) or is_boolean_keyword(peekTok) or isNumeric(peekTok) or peekTok.getType() == MINUS)
            parseExpression(parser)
        elsif(isInt(peekTok) or isFloat(peekTok))
            parseExpression(parser)
        elsif(is_string_or_char(peekTok))
            parseExpression(parser)
        else
            unexpectedToken(parser)
        end
        i = @ifstatement
        # if i.nil?
        #     puts("i is nil")
        # else
        #     puts("i is not nil --------------")
        # end
        reset()
        isnt_unless()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        # if i.nil?
        #     puts("i is still nil")
        # else
        #     puts("i is still not nil --------------")
        # end
        puts(" done parsing conditional")
        return i
    end
    
    def letStep(parser)
        @ifstatement.is_let()
        preOptStep(parser)
    end

    def varStep(parser)
        @ifstatement.is_var()
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
        @ifstatement.set_unwrapped_var(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == EQUAL)
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
        @ifstatement.set_option(parser.nextToken())
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
        @ifstatement.set_ast(@expression_parser.parse_expression())
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
        i = @ifstatement
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            treat_elif_and_else_as_not_nested = true
            if(@is_unless)
                # "unless" not allowed to be in branching statement chains
                treat_elif_and_else_as_not_nested = false
            end
            stmts = @statement_parser.parse(parser, false, treat_elif_and_else_as_not_nested)
            @statements = stmts
            
            peekTok = parser.peek()
        end
        #puts("done parsing statements, in unless statement? #{@is_unless}")
        i.set_statements(@statements)
        @ifstatement = i
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@statements.length() == 0)
                emptyStatement(parser)
            else
                endStep(parser)
            end
        elsif(peekTok.getType() == ELIF)
            return
        elsif(peekTok.getType() == ELSE)
            return
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        if(@is_unless)
            puts("unless is discarding end here")
        else
            puts("if is discarding end here")
        end
        parser.discard()
    end

    def reset()
        @expression_ast = nil
        @statements = Array.new
        @let = false
        @var = false
        @unwrapped_var = nil
        @opt_variable = nil
        @ifstatement = nil
    end

    def enforceIf(token)
        if(token.getText().upcase != IF)
            throw Exception.new("Did not enounter \"if\" keyword in file " + token.getFilename())
        end
    end
end
