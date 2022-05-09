require_relative './parserutilities.rb'
require_relative '../tokentype.rb'


class DefineParser

    def initialize()
        @oldNameToken = nil
        @newNameToken = nil
    end


    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceDefine(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            oldNameStep(parser)
        else
            invalidItemName(parser)
        end
        return defineStatement()
    end

    def oldNameStep(parser)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        end
        @oldNameToken = peekTok
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
        result = DefineStatement.new(@oldNameToken, @newNameToken)
        reset()
        return result
    end

    def enforceDefine(peekTok)
        if(peekTok.getText().upcase != DEFINE)
            throw Exception.new("Did not enounter \"define\" keyword in file " + peekTok.getFilename())
        end
    end

    def reset()
        @oldNameToken = nil
        @newNameToken = nil
    end
end


class DefineStatement
    def initialize(oldName, newName)
        @oldNameToken = oldName
        @newNameToken = newName
    end

    def toJSON()
        return {
            "type" => "define",
            "old_name" => {
                "literal" => @oldNameToken.getText(),
                "type" => @oldNameToken.getType(),
                "line_number" => @oldNameToken.getLine()
            },
            "new_name" => {
                "literal" => @newNameToken.getText(),
                "type" => @newNameToken.getType(),
                "line_number" => @newNameToken.getLine()
            }
        }
    end

    def _printLiteral
        return "old name: #{@oldNameToken.getText()} new name: #{@newNameToken.getText()}"
    end

    def _printTokType(item_list)
        item_list.append(@oldNameToken.getType())
        item_list.append(@newNameToken.getType())
    end
end