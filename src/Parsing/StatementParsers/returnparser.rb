require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class ReturnParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @return_expression = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceReturn(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        end
        r = ReturnStatement.new(@return_expression)
        reset()
        return r
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


class ReturnStatement
    def initialize(return_expression)
        @return_expression = return_expression
    end
end