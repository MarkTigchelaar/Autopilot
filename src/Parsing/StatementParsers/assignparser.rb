require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class AssignParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @name = nil
        @type = nil
        @expression_ast = nil
    end

    def parse(parser)
        reset()
        # let or var handled by statement parser already.
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            variableStep(parser)
        else
            unexpectedToken(parser)
        end
        r = AssignmentStatement.new(@name, @type, @expression_ast)
        reset()
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
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(!is_interal_statement_keyword(peekTok) and !isValidIdentifier(peekTok))
            unexpectedToken(parser)
        end
    end

    def reset()
        @name = nil
        @type = nil
        @expression_ast = nil
    end
end



class AssignmentStatement
    def initialize(name, type, expression_ast)
        @name = name
        @type = type
        @expression_ast = expression_ast
        @let = false
        @var = false
    end

    def usesLet
        @let = true
    end

    def usesVar
        @var = true
    end

    def _printLiteral
        ownership_type = ''
        if(@var)
            ownership_type = "var"
        elsif(@let)
            ownership_type = "let"
        end
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