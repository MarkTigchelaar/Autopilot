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

    def fieldCommaStep(parser)
        # reuse is Step, is doing the same thing
        isStep(parser)
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
        elsif(isValidIdentifier(peekTok) or isPrimitiveType(peekTok, true))
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
            fieldCommaStep(parser)
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
        elsif(peekTok.getType() == FUN)
            funStep(parser, true)
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
        @interfaces = Array.new
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

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "type" => {
                "literal" => @type.getText(),
                "type" => @type.getType(),
                "line_number" => @type.getLine()
            },
            "public" => @is_public
        }
    end

    def _printTokType(type_list)
        if(@is_public)
            type_list.append(PUB)
        end
        type_list.append(@name.getType())
        type_list.append(@type.getType())
    end

    def _printLiteral()
        str = ""
        if(@is_public)
            str += "pub "
        end
        str += @name.getText() + " "
        str += @type.getText() + " "
        return str
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

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "struct",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "attributes" => {
                "acyclic" => @is_acyclic,
                "public" => @is_public,
                "inline" => @is_inline
            },
            "interfaces" => getInterfacesJSON(),
            "fields" => getFieldsJSON(),
            "functions" => getFunctionsJSON()
        }
    end

    def getInterfacesJSON()
        interfaces = Array.new()
        for i in @interfaces
            interfaces.append({
                "literal" => i.getText(),
                "type" => i.getType(),
                "line_number" => i.getLine()
            })
        end
        return interfaces
    end

    def getFieldsJSON()
        fields = Array.new()
        for f in @fields
            fields.append(f.toJSON())
        end
        return fields
    end

    def getFunctionsJSON()
        fns = Array.new()
        for f in @functions
            fns.append(f.toJSON())
        end
        return fns
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
        type_list.append(@name.getType())
        for i in @interfaces
            type_list.append(i.getType())
        end
        for field in @fields
            field._printTokType(type_list)
        end
        for fun in @functions
            fun._printTokType(type_list)
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
            astString += "pub "
        end
        astString += @name.getText() + " "
        for i in @interfaces
            astString += i.getText() + " "
        end
        for field in @fields
            astString += field._printLiteral()
        end
        for fun in @functions
            astString += " " + fun._printLiteral()
        end
        astString = astString.strip()
        astString = astString.squeeze(" ")
        return astString
    end
end