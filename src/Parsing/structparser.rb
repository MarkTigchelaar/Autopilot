require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'


class StructParser
    def initialize(function_parser)
        @function_parser = function_parser
        @name = nil
        @interfaces = Array.new
        @fields = Array.new
        @functions = Array.new
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceStruct(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            structNameStep(parser)
        else
            unexpectedToken(parser)
        end
        s = StructStatement.new(@name, @interfaces, @fields, @functions)
        reset()
        return s
    end

    def structNameStep(parser)
        token = parser.nextToken()
        @name = token
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IS)
            isStep(parser)
        elsif(peekTok.getType() == USES)
            usesStep(parser)    
        else
            unexpectedToken(parser)
        end
    end

    def usesStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            interfaceStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def interfaceStep(parser)
        token = parser.nextToken()
        @interfaces.append(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IS)
            isStep(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
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
            interfaceStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def isStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == PUB)
            pubFieldStep(parser)
        elsif(isValidIdentifier(peekTok))
            fieldNameStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def pubFieldStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            fieldNameStep(parser, true)
        else
            unexpectedToken(parser)
        end
    end

    def fieldNameStep(parser, is_public = false)
        nameToken = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == AS)
            asStep(parser, is_public, nameToken)
        else
            unexpectedToken(parser)
        end 
    end

    def asStep(parser, is_public, nameToken)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            fieldTypeStep(parser, is_public, nameToken)
        else
            unexpectedToken(parser)
        end
    end

    def fieldTypeStep(parser, is_public, nameToken)
        typeToken = parser.nextToken()
        field = StructField.new(nameToken, typeToken, is_public)
        @fields.append(field)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        elsif(peekTok.getType() == ACYCLIC)
            acyclicStep(parser)
        elsif(peekTok.getType() == PUB)
            pubFunctionStep(parser)
        elsif(peekTok.getType() == FUN)
            funStep(parser)
        else
            unexpectedToken(parser)
        end 
    end

    def acyclicStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == PUB)
            pubFunctionStep(parser, true)
        else
            unexpectedToken(parser)
        end
    end

    def pubFunctionStep(parser, is_acyclic = false)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == FUN)
            funStep(parser, is_acyclic, true)
        else
            unexpectedToken(parser)
        end
    end

    def funStep(parser, is_acyclic = false, is_public = false)
        func = @function_parser.parse(parser)
        if(is_acyclic)
            func.setAsAcyclic()
        end
        if(is_public)
            func.setAsPublic()
        end
        @functions.append(func)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        elsif(peekTok.getType() == ACYCLIC)
            acyclicStep(parser)
        elsif(peekTok.getType() == PUB)
            pubFunctionStep(parser)
        elsif(peekTok.getType() == FUN)
            funStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def reset()
        @name = nil
        @fields = Array.new
        @functions = Array.new
    end

    def endStep(parser)
        parser.discard()
    end

    def enforceStruct(token)
        if(token.getText().upcase != STRUCT)
            throw Exception.new("Did not enounter \"struct\" keyword in file " + token.getFilename())
        end
    end
end


class StructField
    def initialize(name, type, is_public)
        @name = name
        @type = type
        @is_public = is_public
    end
end

class StructStatement
    def initialize(name, interfaces, fields, functions)
        @name = name
        @interfaces = interfaces
        @fields = fields
        @functions = functions
        @is_acyclic = false
        @is_public = false
        @is_inline = false
    end

    def setAsAcyclic
        @is_acyclic = true
    end

    def setAsPublic
        @is_public = true
    end

    def setAsInline
        @is_inline = true
    end
end