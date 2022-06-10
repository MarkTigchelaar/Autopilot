require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


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
        elsif(isValidIdentifier(peekTok) or is_valid_r_value_keyword(peekTok))
            parseExpression(parser)
        else
            puts "HERE!!!!!!!"
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

class WhileStatement
    def initialize(loop_name, expression_ast, statements)
        @loop_name = loop_name
        @expression_ast = expression_ast
        @statements = statements
    end

    def toJSON()
        puts "IN HERE!"
        return {
            "name" => get_name(),
            "expression" => @expression_ast.toJSON(),
            "statements" => @statements.toJSON()
        }
    end

    def get_name()
        lit = ""
        lit = @loop_name.getText() if @loop_name
        type = ""
        type = @loop_name.getType() if @loop_name
        line = ""
        line = @loop_name.getLine() if @loop_name
        {
            "literal" => lit,
            "type" => type,
            "line_number" => line
        }
    end

    def _printTokType(type_list)
        if(@loop_name != nil)
            type_list.append(@loop_name.getType())
        end
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        end
        @statements._printTokType(type_list)
    end

    def _printLiteral()
        l = Array.new
        @expression_ast._printLiteral(l)
        msg = "exp: " + l.join("")
        name = ""
        if(@loop_name != nil)
            name = "name: " + @loop_name.getText() + ", "
        end
        return name + msg
    end
end