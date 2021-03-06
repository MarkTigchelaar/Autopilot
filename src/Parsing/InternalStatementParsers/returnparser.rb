require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/return_statement.rb'

class ReturnParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @return_expression = nil
    end

    def parse(parser)
        reset()
        @expression_parser.loadTokenizer(parser)
        token = parser.nextToken()
        enforceReturn(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseExpression(parser)
        end
        r = ReturnStatement.new(@return_expression)
        reset()
        return r
    end

    def parseExpression(parser)
        @return_expression = @expression_parser.parse_expression()
    end

    def enforceReturn(token)
        if(token.getText().upcase != RETURN)
            throw Exception.new("Did not enounter \"return\" keyword in file " + token.getFilename())
        end
    end

    def reset()
        @return_expression = nil
    end
end
