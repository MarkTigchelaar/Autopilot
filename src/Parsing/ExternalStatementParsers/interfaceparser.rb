require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/interface_statement.rb'

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
