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
        @unwrapped_var = nil
        @opt_variable = nil
        @is_unless = false
    end

    def is_unless()
        @is_unless = true
    end

    def isnt_unless()
        @is_unless = false
    end

    def parse(parser)
        reset()
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
        else
            parseExpression(parser)
        end
        i = IfStatement.new(@let, @var, @unwrapped_var, @opt_variable, @expression_ast, @statements)
        reset()
        isnt_unless()
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
        @unwrapped_var = token
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
        @opt_variable = parser.nextToken()
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
        puts "parsing expression"
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            puts "Found unexpected token"
            unexpectedToken(parser)
        end
    end

    def parseStatements(parser)
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

    def reset()
        @expression_ast = nil
        @statements = Array.new
        @let = false
        @var = false
        @unwrapped_var = nil
        @opt_variable = nil
    end

    def enforceIf(token)
        if(token.getText().upcase != IF)
            throw Exception.new("Did not enounter \"if\" keyword in file " + token.getFilename())
        end
    end
end


class IfStatement
    def initialize(let, var, unwrapped_var, option, expression_ast, statements)
        @let = let
        @var = var
        @unwrapped_var = unwrapped_var
        @option = option
        @expression_ast = expression_ast
        @statements = statements
    end

    def _printTokType(type_list)
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        end
        if(@var)
            type_list.append(" var")
        elsif(@let)
            type_list.append(" let")
        end
        if(@var or @let)
            type_list.append(" #{@unwrapped_var.getText()}: #{@option.getText()}")
        end

    end

    def get_ast()
        return @expression_ast
    end

    def get_statements()
        return @statements
    end

    def _printLiteral()
        if(@expression_ast != nil)
            l = Array.new
            @expression_ast._printLiteral(l)
            return "exp:" + l.join("")
        end
        type = ""
        if(@var)
            type = "var"
        elsif(@let)
            type = "let"
        end
        msg = ""
        if(@var or @let)
            msg = " #{@unwrapped_var.getText()}: #{@option.getText()}"
        end
        return type + msg
    end
end