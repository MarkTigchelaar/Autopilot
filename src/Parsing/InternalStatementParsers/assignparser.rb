require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/assign_statement.rb'

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
        elsif(isValidIdentifier(peekTok) or is_boolean_keyword(peekTok) or isNumeric(peekTok) or peekTok.getType() == MINUS)
            parseExpression(parser)
        elsif(isInt(peekTok) or isFloat(peekTok))
            parseExpression(parser)
        elsif(is_string_or_char(peekTok))
            parseExpression(parser)
        else
            unexpectedToken(parser)
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
