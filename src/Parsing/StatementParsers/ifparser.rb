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
        reset()
        @ifstatement = IfStatement.new()
        token = parser.nextToken()
        enforceIf(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            #puts "EOF line 33"
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
        i = @ifstatement #IfStatement.new(@let, @var, @unwrapped_var, @opt_variable, @expression_ast, @statements)
        reset()
        isnt_unless()
        return i  
    end
    
    def letStep(parser)
        #@let = true
        @ifstatement.is_let()
        preOptStep(parser)
    end

    def varStep(parser)
        #@var = true
        @ifstatement.is_var()
        preOptStep(parser)
    end

    def preOptStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            #puts "EOF line 70"
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            optionUnwrappedVarStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def optionUnwrappedVarStep(parser)
        token = parser.nextToken()
        #@unwrapped_var = token
        @ifstatement.set_unwrapped_var(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            #puts "EOF line 84"
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
            #puts "EOF line 97"
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            optionNameStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def optionNameStep(parser)
        #@opt_variable = parser.nextToken()
        @ifstatement.set_option(parser.nextToken())
        peekTok = parser.peek()
        if(isEOF(peekTok))
            #puts "EOF line 110"
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
            #puts "EOF line 123"
            eofReached(parser)
        else
            parseStatements(parser)
        end
    end

    def parseExpression(parser)
        #puts "parsing expression"
        @expression_parser.loadTokenizer(parser)
        #@expression_ast = 
        @ifstatement.set_ast(@expression_parser.parse_expression())
        peekTok = parser.peek()
        if(isEOF(peekTok))
            #puts "EOF line 136"
            eofReached(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            #puts "Found unexpected token"
            unexpectedToken(parser)
        end
    end

    def parseStatements(parser)
        #puts "PARSING STATEMENTS!!!!!!!!!!!!!!!!"
        peekTok = parser.peek()
        #puts "peekToken in if parser, parse statements: #{peekTok.getText()}"
        i = @ifstatement
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            
            #puts "PARSING IF STATEMENTS SUB STATEMENTS!!!"
            stmts = @statement_parser.parse(parser)
            @statements = stmts
            #puts "DONE PARSING IF STATEMENTS SUB STATEMENTS!!!"
            
            peekTok = parser.peek()
            if(parser.hasErrors())
                #puts "parser has errors:"
                for e in parser.getErrorList()
                    #puts "Error: #{e["tokenLiteral"]}"
                    #puts "message: #{e["message"]}"
                end
                return
            end
        end
        @ifstatement = i
        #puts "RETURNED !!"
        if(isEOF(peekTok))
            #puts "EOF line 158"
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            #puts "Found end scope"
            if(@statements.length() == 0)
                #puts "statements length is 0"
                emptyStatement(parser)
            else
                #puts "end step"
                endStep(parser)
            end
        else
            #puts "unexpected token at line 177, if parser"
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
        @ifstatement = nil
    end

    def enforceIf(token)
        if(token.getText().upcase != IF)
            throw Exception.new("Did not enounter \"if\" keyword in file " + token.getFilename())
        end
    end
end


class IfStatement
     
    #def initialize(let, var, unwrapped_var, option, expression_ast, statements)
    def initialize()
        @let = false#let
        @var = false
        @unwrapped_var = nil#unwrapped_var
        @option = nil#option
        @expression_ast = nil#expression_ast
        @statements = nil#statements
    end

    def set_unwrapped_var(opt)
        @unwrapped_var
    end

    def set_option(opt)
        @option
    end

    def is_let()
        @let = true
    end

    def is_var()
        @var = true
    end

    def set_ast(ast)
        @expression_ast = ast
    end

    def get_ast()
        return @expression_ast
    end

    def set_statements(stmts)
        @statements = stmts
    end

    def get_statements()
        return @statements
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