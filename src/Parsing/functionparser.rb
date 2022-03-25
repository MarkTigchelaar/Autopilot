require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'

class FunctionParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new()
        @function_name = nil
        @arguments = Array.new()
        @return_type = nil
        @keywords = getkeywords()
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
        elsif(isValidIdentifier(peekTok))
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
        elsif(peekTok.getType() == EQUAL_EQUAL)
            assignStep(parser, argname, argtype)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def assignStep(parser, argname, argtype)
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
            argTypeStep(parser, argname)
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
            returnTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def doStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isKeyword(peekTok) and peekTok.getType() != ENDSCOPE)
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
        while(!isEOF(peekTok) and peekTok.getType() != ENDSCOPE)
            @statements.append(@statement_parser.parse(parser))
        end
        peekTok = parser.peek()
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

    def isEOF(token)
        return token.getType() == EOF
    end

    def addError(parser, message)
        #puts "ADDING ERROR"
         parser.addError(parser.nextToken(), message)
         parser.setToSync()
     end
 
     def eofReached(parser)
         msg = "End of file reached."
         addError(parser, msg)
     end

     def unexpectedToken(parser)
        msg = "Unexpected token #{parser.peek().getText()}."
        addError(parser, msg)
    end

    def isValidIdentifier(token)
        if(isKeyword(token))
            return false
        end
        return isIdentifier(token)
    end

    def isKeyword(token)
        if(@keywords.has_key?(token.getText()))
            return true
        end
        return false
    end

    def reset()
        @statements = Array.new()
        @function_name = nil
        @arguments = Array.new()
        @return_type = nil
    end
end

class FunctionArgument
    def initialize(var_name, var_type, default_value = nil)
        @var_name = var_name
        @var_type = var_type
        @default_value = default_value
    end
end

class FunctionStatement
    def initialize(function_name, arguments, return_type, statements)
        @function_name = function_name
        @arguments = arguments
        @return_type = return_type
        @statements = statements
        @is_acyclic = false
        @is_public = false
    end

    def setAsAcyclic()
        @is_acyclic = true
    end

    def setAsPublic()
        @is_public = true
    end
end