require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

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
        elsif(isValidIdentifier(peekTok))
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
        elsif(isValidIdentifier(peekTok))
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
        elsif(isValidIdentifier(peekTok))
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

class ForStatement
    def initialize(loop_name, let, var, var_one, var_two, opt_variable, start_collection_ast, stop_collection_ast, statements)
        @loop_name = loop_name
        @start_collection_ast = start_collection_ast
        @stop_collection_ast = stop_collection_ast
        @statements = statements
        @let = let
        @var = var
        @var_one = var_one
        @var_two = var_two
        @opt_variable = opt_variable
    end

    def _printLiteral()
        lit = ""
        if @let
            lit += "let "
        elsif @var
            lit += "var "
        end
        if @var_one
            lit += @var_one.getText() + ' '
        end
        if @var_two
            lit += @var_two.getText() + ' '
        end
        if @opt_variable
            lit += @opt_variable.getText() + ' '
        end
        if @start_collection_ast != nil
            l = Array.new
            ast = @start_collection_ast
            ast._printLiteral(l)
            lit += l.join(" ") + ' '
        end
        if @stop_collection_ast != nil
            l = Array.new
            ast = @stop_collection_ast
            ast._printLiteral(l)
            lit += l.join(" ") + ' '
        end
        if(@loop_name != nil)
            lit += @loop_name.getText() + ' '
        end
        if @statements != nil
            for stmt in @statements
                lit += stmt._printLiteral() + ' '
            end
        end
        return lit.strip()
    end

    def _printTokType(type_list)
        if @let
            type_list.append("let")
        elsif @var
            type_list.append("var")
        end
        if @var_one
            type_list.append(@var_one.getType())
        end
        if @var_two
            type_list.append(@var_two.getType())
        end
        if @opt_variable
            type_list.append(@opt_variable.getType())
        end
        if(@loop_name != nil)
            type_list.append(@loop_name.getType())
        end
        if @start_collection_ast != nil
            ast = @start_collection_ast
            ast._printTokType(type_list)
        end
        if @stop_collection_ast != nil
            ast = @stop_collection_ast
            ast._printTokType(type_list)
        end
        if @statements != nil
            for stmt in @statements
                stmt._printTokType(type_list)
            end
        end
    end
end