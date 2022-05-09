require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class AssignParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @name = nil
        @type = nil
        @let_or_var = nil
        @expression_ast = nil
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        @let_or_var = parser.nextToken()
        enforceAssign()

        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            variableStep(parser)
        else
            unexpectedToken(parser)
        end
        r = AssignmentStatement.new(@let_or_var, @name, @type, @expression_ast)
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        return r
    end

    def variableStep(parser)
        @name = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        elsif(peekTok.getType() == EQUAL)
            equalStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def asStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isPrimitiveType(peekTok, true))
            typeStep(parser)
        elsif(isValidIdentifier(peekTok))
            typeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def typeStep(parser)
        @type = parser.nextToken()
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
        else
            parseExpression(parser)
        end
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
    end

    def reset()
        @name = nil
        @type = nil
        @expression_ast = nil
        @let_or_var = nil
    end

    def enforceAssign()
        if(@let_or_var.getType() != LET and @let_or_var.getType() != VAR)
            raise Exception.new("Did not enounter \"let\" or \"var\" keywords in file " + @let_or_var.getFilename())
        end
    end
end



class AssignmentStatement
    def initialize(let_or_var, name, type, expression_ast)
        @name = name
        @type = type
        @expression_ast = expression_ast
        @let_or_var = let_or_var
    end

    def toJSON()
        return {
            "type" => "assignment",
            "token" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "variable_type" => {
                "literal" => @type.getText(),
                "type" => @type.getType(),
                "line_number" => @type.getLine()
            },
            "assignment_type" => @let_or_var.getType(),
            "rvalue" => @expression_ast.toJSON()
        }
    end

    def usesLet
        @let = true
    end

    def usesVar
        @var = true
    end

    def _printLiteral
        ownership_type = @let_or_var.getText()
        if(@expression_ast != nil)
            l = Array.new
            @expression_ast._printLiteral(l)
            if(@type != nil)
                t = @type.getText()
            else
                t = ""
            end
            return "name: #{@name.getText()}, type: #{t}, ownership type: #{ownership_type}, exp: " + l.join("")
        else
            raise Exception.new("Expression not found.")
        end
    end

    def _printTokType(type_list)
        type_list.append(@name.getType())
        if(@type != nil)
            type_list.append(@type.getType())
        end
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        else
            raise Exception.new("Expression not found.")
        end
    end
end