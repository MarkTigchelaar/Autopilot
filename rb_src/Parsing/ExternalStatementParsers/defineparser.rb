require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/define_statement.rb'

class DefineParser
    def initialize()
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
            FIFOQUEUE,
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
        @explicitTypeDef.addSubType(LinearType.new(peekTokType))
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
        result = DefineStatement.new(@newNameToken, @explicitTypeDef)
        reset()
        return result
    end

    def enforceDefine(peekTok)
        if(peekTok.getText().upcase != DEFINE)
            throw Exception.new("Did not enounter \"define\" keyword in file " + peekTok.getFilename())
        end
    end

    def reset()
        @newNameToken = nil
        @explicitTypeDef = nil
    end
end
