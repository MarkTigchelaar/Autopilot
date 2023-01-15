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
        #puts("parsing return")
        reset()
        @expression_parser.loadTokenizer(parser)
        token = parser.nextToken()
        enforceReturn(token)
        peekTok = parser.peek()
        puts("peek token in return parser: #{peekTok.getText()}")
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or is_boolean_keyword(peekTok) or isNumeric(peekTok) or peekTok.getType() == MINUS)
            parseExpression(parser)
        elsif(isInt(peekTok) or isFloat(peekTok))
            parseExpression(parser)
        elsif(is_string_or_char(peekTok))
            parseExpression(parser)
        # not a if, else, end etc.
        elsif(!isGeneralKeyWord(peekTok.getText()))
            unexpectedToken(parser)
        end
        r = ReturnStatement.new(token, @return_expression)
        reset()
        puts("done parsing return")
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
