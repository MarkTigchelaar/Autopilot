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
        reset()
        # let or var handled by statement parser already.
        @let_or_var = parser.nextToken()

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
        #puts "RETURNING FROM PARSE ASSIGN STATEMENT----------------"
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
        #puts "Parsing expression ------------------------------------- has errors? #{parser.hasErrors()}"
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
        #puts "parsed expression has errors? #{parser.hasErrors()}"
    end

    def reset()
        @name = nil
        @type = nil
        @expression_ast = nil
        @let_or_var = nil
    end
end



class AssignmentStatement
    def initialize(let_or_var, name, type, expression_ast)
        @name = name
        @type = type
        @expression_ast = expression_ast
        @let_or_var = let_or_var
    end

    def usesLet
        @let = true
    end

    def usesVar
        @var = true
    end

    def _printLiteral
        ownership_type = @let_or_var.getText()
        #if(@var)
        #    ownership_type = "var"
        #elsif(@let)
        #    ownership_type = "let"
        #end
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