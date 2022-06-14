require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../Tokenization/token.rb'

class InterfaceParser

    def initialize(function_parser)
        @function_parser = function_parser
        @functions = Array.new()
        @interface_name = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceInterface(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            interfaceNameStep(parser)
        else
            unexpectedToken(parser)
        end

        i = InterfaceStatement.new(@interface_name, @functions)
        reset()
        return i
    end

    def interfaceNameStep(parser)
        @interface_name = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IS)
            isStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def isStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == FUN or peekTok.getType() == ACYCLIC)
            parseFunctions(parser)
        else
            unexpectedToken(parser)
        end
    end

    def parseFunctions(parser)
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (peekTok.getType() == FUN or peekTok.getType() == ACYCLIC))
            is_acyclic = false
            if(peekTok.getType() == ACYCLIC)
                parser.discard()
                peekTok = parser.peek()
                if(peekTok.getType() != FUN)
                    unexpectedToken(parser)
                    break
                end
                is_acyclic = true
            end
            @function_parser.inInterface()
            fn = @function_parser.parse(parser)
            @function_parser.outInterface()
            if(is_acyclic)
                fn.setAsAcyclic()
            end
            # functions in interfaces are always public
            fn.setAsPublic()
            @functions.append(fn)
            peekTok = parser.peek()
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@functions.length() == 0)
                noFunctions(parser)
            else
                endStep(parser)
            end
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def enforceInterface(token)
        if(token.getText().upcase != INTERFACE)
            throw Exception.new("Did not enounter \"interface\" keyword in file " + token.getFilename())
        end
    end

    def reset()
        @functions = Array.new()
        @function_name = nil
        @arguments = Array.new()
        @return_type = nil
    end
end


class InterfaceStatement
    def initialize(name, functions)
        @name = name
        @functions = functions
        @is_acyclic = false
        @is_public = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "interface",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "functions" => getFunctionsJSON(),
            "attributes" => {
                "acyclic" => @is_acyclic,
                "public" => @is_public
            }
        }
    end

    def getFunctionsJSON()
        funcs = Array.new()
        for fn in @functions
            funcs.append(fn.toJSON())
        end
        return funcs
    end

    def setAsAcyclic()
        @is_acyclic = true
    end

    def setAsPublic()
        @is_public = true
    end

    def _printTokType(type_list)
        if(@is_acyclic)
            type_list.append(ACYCLIC)
        end
        if(@is_public)
            type_list.append(PUB)
        end
        type_list.append(@name.getType())
        for func in @functions
            func._printTokType(type_list)
        end
    end

    def _printLiteral()
        astString = ""
        if(@is_acyclic)
            astString += "acyclic "
        end
        if(@is_public)
            astString += "pub "
        end
        astString += @name.getText() + " "
        for func in @functions
            astString += func._printLiteral() + " "
        end
        astString = astString.strip()
        astString = astString.squeeze(" ")
        return astString
    end
end