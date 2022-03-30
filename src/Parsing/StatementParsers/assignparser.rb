require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class AssignParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @name = nil
        @expression_ast = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceLetOrVar(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            variableStep(parser)
        else
            unexpectedToken(parser)
        end
        r = AssignmentStatement.new(@name, @expression_ast)
        reset()
        return r
    end

    def variableStep(parser)
        parser.discard()
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

    def enforceLetOrVar(token)
        if(token.getText().upcase != LET and token.getText().upcase != VAR)
            throw Exception.new("Did not enounter \"let\" or \"var\" keywords in file " + token.getFilename())
        end
    end

    def reset()
        @name = nil
        @expression_ast = nil
    end
end



class AssignmentStatement
    def initialize(name, expression_ast)
        @name = name
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
end