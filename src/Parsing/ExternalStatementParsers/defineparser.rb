require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/define_statement.rb'

class DefineParser

    def initialize()
        #@oldNameToken = nil
        @explicitTypeDef = nil
        @newNameToken = nil
        @linear_types = [
            LIST, 
            LINKEDLIST, 
            VECTOR, 
            SET, 
            HASHSET, 
            TREESET, 
            STACK, 
            QUEUE,
            PRIORITYQUEUE,
            DEQUE,
            OPTION # technically not a linear type, but steps are the same
        ]
        @key_value_types = [
            MAP,
            DICTIONARY,
            HASHMAP
        ]
    end

    def parse(parser)
        reset()
        @explicitTypeDef = TypeDef.new()
        token = parser.nextToken()
        enforceDefine(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(@key_value_types.include?(peekTok.getType()))
            keyValueTypeStep(parser, peekTok)
        elsif(@linear_types.include?(peekTok.getType()))
            linearContainerTypeStep(parser, peekTok)
        elsif(peekTok.getType() == RESULT)
            resultStep(parser, peekTok)
        elsif(peekTok.getType() == FUN)
            functionSignatureStep(parser, peekTok)
        elsif(isValidIdentifier(peekTok))
            oldNameStep(parser)
        else
            invalidItemName(parser)
        end
        return defineStatement()
    end

    def keyValueTypeStep(parser, peekTokType)
        @explicitTypeDef.addSubType(KeyValueType.new(peekTokType))
        #@explicitTypeDef.addTypeToken(peekTokType)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            leftParenMapStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def linearContainerTypeStep(parser, peekTokType)
        #raise Exception.new("Not implemented")
        @explicitTypeDef.addSubType(LinearType.new(peekTokType))
        #@explicitTypeDef.addTypeToken(peekTokType)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            leftParenLinearStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def leftParenLinearStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            linearTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def linearTypeStep(parser)
        linearTypeToken = parser.nextToken()
        @explicitTypeDef.addLinearTypeToken(linearTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def resultStep(parser, peekTokType)
        
        @explicitTypeDef.addSubType(ResultType.new(peekTokType))
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            leftParenResultStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def leftParenResultStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            resultTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def resultTypeStep(parser)
        resultTypeToken = parser.nextToken()
        @explicitTypeDef.addResultTypeToken(resultTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            resultCommaStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def resultCommaStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            resultErrorTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def resultErrorTypeStep(parser)
        errorTypeToken = parser.nextToken()
        @explicitTypeDef.addResultErrorTypeToken(errorTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def functionSignatureStep(parser, peekTokType)
        #raise Exception.new("Not implemented")
        
        @explicitTypeDef.addSubType(FunctionType.new(peekTokType))
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            leftParenFunctionStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def leftParenFunctionStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            functionArgTypeStep(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            functionRightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def functionArgTypeStep(parser)
        funcArgTypeToken = parser.nextToken()
        @explicitTypeDef.addFunctionArgToken(funcArgTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            funcCommaStep(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            functionRightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def funcCommaStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            functionArgTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def functionRightParenStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            functionReturnTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def functionReturnTypeStep(parser)
        funcReturnTypeToken = parser.nextToken()
        @explicitTypeDef.addFunctionReturnTypeToken(funcReturnTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def leftParenMapStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            mapKeyTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def mapKeyTypeStep(parser)
        keyTypeToken = parser.nextToken()
        @explicitTypeDef.addMapKeyToken(keyTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COLON)
            mapColonStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def mapColonStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
            mapValueTypeStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def mapValueTypeStep(parser)
        valueTypeToken = parser.nextToken()
        @explicitTypeDef.addMapValueToken(valueTypeToken)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def rightParenStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def oldNameStep(parser)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        end
        
        @explicitTypeDef.addSubType(RenameType.new(peekTok))
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def asStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            newNameStep(parser)
        else
            invalidItemName(parser)
        end
    end

    def newNameStep(parser)
        name = parser.nextToken()
        if(!isValidIdentifier(name))
            invalidItemName(parser)
        else
            @newNameToken = name
        end
    end

    def defineStatement()
        result = DefineStatement.new(
            #@oldNameToken, 
            @newNameToken, @explicitTypeDef)
        reset()
        return result
    end

    def enforceDefine(peekTok)
        if(peekTok.getText().upcase != DEFINE)
            throw Exception.new("Did not enounter \"define\" keyword in file " + peekTok.getFilename())
        end
    end

    def reset()
        #@oldNameToken = nil
        @newNameToken = nil
        @explicitTypeDef = nil
    end
end



















class KeyValueType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @key_token = nil
        @value_token = nil
    end

    def add_key_token(key_token)
        @key_token = key_token
    end

    def add_value_token(value_token)
        @value_token = value_token
    end

    def _printLiteral
        @tokenTypeToken.getText() + "(" + @key_token.getText() + ":" + @value_token.getText() + ")"
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        item_list.append(@key_token.getType())
        item_list.append(@value_token.getType())
    end

    def toJSON()

    end
end

class LinearType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @value_token = nil
    end

    def add_value_token(value_token)
        @value_token = value_token
    end

    def _printLiteral
        @tokenTypeToken.getText() + "(" + @value_token.getText() + ")"
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        item_list.append(@value_token.getType())
    end

    def toJSON()

    end
end

class RenameType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken
    end

    def _printLiteral
        @tokenTypeToken.getText()
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
    end

    def toJSON()
        {
            "literal" => @tokenTypeToken.getText(),
            "type" => @tokenTypeToken.getType(),
            "line_number" => @tokenTypeToken.getLine()
        }
    end
end

class ResultType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @value_token = nil
        @error_type_token = nil
    end

    def add_value_token(value_token)
        @value_token = value_token
    end

    def add_error_type_token(error_type_token)
        @error_type_token = error_type_token
    end

    def _printLiteral
        @tokenTypeToken.getText + "(" + @value_token.getText() + "," + @error_type_token.getText() + ")"
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        item_list.append(@value_token.getType())
        item_list.append(@error_type_token.getType())
    end

    def toJSON()

    end
end

class FunctionType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @return_type_token = nil
        @arg_types_list = Array.new()
    end

    def add_arg_type_token(value_token)
        @arg_types_list.append(value_token)
    end

    def add_return_type_token(return_type_token)
        @return_type_token = return_type_token
    end

    def _printLiteral
        args = ""
        @arg_types_list.each do |arg|
            args += arg.getText() + ","
        end
        args = args.delete_suffix(",")
        @tokenTypeToken.getText() + "(" + args + ")" + @return_type_token.getText()
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        @arg_types_list.each do |arg|
            item_list.append(arg.getType())
        end
        item_list.append(@return_type_token.getType())
    end

    def toJSON()

    end
end

class TypeDef
    def initialize()
        @sub_container = nil
    end

    def addSubType(sub_container)
        @sub_container = sub_container
    end

    def addMapValueToken(valueTypeToken)
        @sub_container.add_value_token(valueTypeToken)
    end

    def addMapKeyToken(keyTypeToken)
        @sub_container.add_key_token(keyTypeToken)
    end
    
    def addFunctionReturnTypeToken(funcReturnTypeToken)
        @sub_container.add_return_type_token(funcReturnTypeToken)
    end

    def addFunctionArgToken(funcArgTypeToken)
        @sub_container.add_arg_type_token(funcArgTypeToken)
    end

    def addResultErrorTypeToken(errorTypeToken)
        @sub_container.add_error_type_token(errorTypeToken)
    end

    def addResultTypeToken(resultTypeToken)
        @sub_container.add_value_token(resultTypeToken)
    end

    def addLinearTypeToken(linearTypeToken)
        @sub_container.add_value_token(linearTypeToken)
    end

    def _printLiteral()
        @sub_container._printLiteral()
    end

    def _printTokType(item_list)
        @sub_container._printTokType(item_list)
    end

    def toJSON()
        @sub_container.toJSON()
    end
end