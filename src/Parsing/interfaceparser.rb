require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'

class InterfaceParser

    def initialize(function_parser)
        @function_parser = function_parser
        @functions = Array.new()
        @interface_name = nil
        @keywords = getkeywords()
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
        parser.discard()
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
            fn = @function_parser.parse(parser)
            if(is_acyclic)
                fn.setAsAcyclic()
            end
            # functions in interfaces are always public
            fn.setAsPublic()
            @functions.append(fn)
            peekTok = parser.peek()
        end
        #peekTok = parser.peek()
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

    def enforceInterface(token)
        if(token.getText().upcase != INTERFACE)
            throw Exception.new("Did not enounter \"interface\" keyword in file " + token.getFilename())
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
    end
end