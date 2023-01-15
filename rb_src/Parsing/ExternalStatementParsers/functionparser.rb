require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/function_statement.rb'

class FunctionParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = nil
        @function_name = nil
        @arguments = Array.new()
        @return_type = nil
        @func_definition = false
    end

    def inInterface()
        @func_definition = true
    end

    def outInterface()
        @func_definition = false
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceFunction(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            functionNameStep(parser)
        else
            unexpectedToken(parser)
        end
        f = FunctionStatement.new(@function_name, @arguments, @return_type, @statements)
        reset()
        return f
    end

    def functionNameStep(parser)
        current = parser.nextToken()
        @function_name = current
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            leftParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def leftParenStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            argNameStep(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def argNameStep(parser)
        argname = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser, argname)
        else
            unexpectedToken(parser)
        end
    end

    def asStep(parser, argname)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            argTypeStep(parser, argname)
        else
            unexpectedToken(parser)
        end
    end

    def argTypeStep(parser, argname)
        argtype = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            @arguments.append(FunctionArgument.new(argname, argtype))
            commaStep(parser)
        elsif(peekTok.getType() == EQUAL)
            assignStep(parser, argname, argtype)
        elsif(peekTok.getType() == RIGHT_PAREN)
            @arguments.append(FunctionArgument.new(argname, argtype))
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def assignStep(parser, argname, argtype)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif([STRING, CHAR, FLOAT, INT].include?(peekTok.getType()))
            addDefaultStep(parser, argname, argtype)
        else
            unexpectedToken(parser)
        end
    end

    def addDefaultStep(parser, argname, argtype)
        default_value = parser.nextToken()
        @arguments.append(FunctionArgument.new(argname, argtype, default_value))
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
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
            argNameStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def rightParenStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@func_definition)
                endStep(parser)
            else
                unexpectedToken(parser)
            end
        elsif(peekTok.getType() == DO)
            doStep(parser)
        elsif(isIdentifier(peekTok))
            if(!isExternalKeyword(peekTok))
                returnTypeStep(parser)
            else
                unexpectedToken(parser)
            end
        else
            unexpectedToken(parser)
        end
    end

    def doStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(is_interal_statement_keyword(peekTok) and peekTok.getType() != ENDSCOPE)
            parseStatements(parser)
        elsif(isAlphaNumericWord(peekTok) and !isExternalKeyword(peekTok))
            parseStatements(parser)
        else
            unexpectedToken(parser)
        end
    end

    def returnTypeStep(parser)
        current = parser.nextToken()
        @return_type = current
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@func_definition)
                endStep(parser)
            else
                unexpectedToken(parser)
            end
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        if(!isEOF(peekTok) and peekTok.getType() != ENDSCOPE)
            @statements = @statement_parser.parse(parser)
        end
        
        peekTok = parser.peek()
        puts("peek token from function parser, in parse statements: #{peekTok.getText()}")
        puts(@statements.toJSON())
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def enforceFunction(token)
        if(token.getText().upcase != FUN)
            throw Exception.new("Did not enounter \"fun\" keyword in file " + token.getFilename())
        end
    end

    def reset()
        @statements = nil
        @function_name = nil
        @arguments = Array.new()
        @return_type = nil
    end
end
