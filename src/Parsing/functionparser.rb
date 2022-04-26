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
        #elsif(peekTok.getType() == STRING or peekTok.getType() == CHAR or peekTok.getType() == FLOAT or peekTok.getType() == INT)
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
        stmts = Array.new()
        if(!isEOF(peekTok) and peekTok.getType() != ENDSCOPE)
            @statements = @statement_parser.parse(parser)
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

    def _printLiteral()
        str =  @var_name.getText() + " " + @var_type.getText()
        if(@default_value != nil)
            return str + " " + @default_value.getText()
        end
        return str
    end

    def _printTokType(type_list)
        type_list.append(@var_name.getType())
        type_list.append(@var_type.getType())
        if(@default_value != nil)
            type_list.append(@default_value.getType())
        end
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
        @is_inline = false
    end

    def setAsAcyclic()
        @is_acyclic = true
    end

    def setAsPublic()
        @is_public = true
    end

    def setAsInline()
        @is_inline = true
    end

    def _printTokType(type_list)
        if(@is_acyclic)
            type_list.append(ACYCLIC)
        end
        if(@is_inline)
            type_list.append(INLINE)
        end
        if(@is_public)
            type_list.append(PUB)
        end
        type_list.append(@function_name.getType())
        for arg in @arguments
            arg._printTokType(type_list)
        end
        if(@return_type != nil)
            type_list.append(@return_type.getType())
        end
        for stmt in @statements
            stmt._printTokType(type_list)
        end
    end

    def _printLiteral()
        astString = ""
        if(@is_acyclic)
            astString += "acyclic "
        end
        if(@is_inline)
            astString += "inline "
        end
        if(@is_public)
            astString += "public "
        end
        astString += @function_name.getText() + " "
        for arg in @arguments
            astString += arg._printLiteral() + " "
        end
        if(@return_type != nil)
            astString += " " + @return_type.getText()
        end
        for stmt in @statements
            astString += " " + stmt._printLiteral()
        end
        astString = astString.strip()
        astString = astString.squeeze(" ")
        return astString
    end
end