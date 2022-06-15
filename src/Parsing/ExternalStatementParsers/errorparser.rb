require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'


class ErrorParser
    def initialize()
        @name = nil
        @itemList = Array.new()
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceError(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            errorNameStep(parser)
        else
            unexpectedToken(parser)
        end
        e = ErrorStatement.new(@name, @itemList)
        reset()
        return e
    end

    def errorNameStep(parser)
        @name = parser.nextToken()
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
        elsif(isValidIdentifier(peekTok))
            errorListItemStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def errorListItemStep(parser)
        token = parser.nextToken()
        @itemList.append(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
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
            errorListItemStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def reset()
        @name = nil
        @itemList = Array.new()
    end

    def enforceError(token)
        if(token.getText().upcase != ERROR)
            throw Exception.new("Did not enounter \"error\" keyword in file " + token.getFilename())
        end
    end
end

class ErrorStatement
    def initialize(name, itemList)
        @name = name
        @items = itemList
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "error",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "error_list" => getErrorsList()
        }
    end

    def getErrorsList
        errs = Array.new()
        for err in @items
            errs.append({
                "literal" => err.getText(),
                "type" => err.getType(),
                "line_number" => err.getLine()
            })
        end
        return errs
    end

    def _printLiteral()
        astString = ""
        astString += @name.getText() + " "
        for item in @items do
            astString += item.getText() + " "
        end
        
        return astString.rstrip()
    end

    def _printTokType(type_list)
        if(@name != nil)
            type_list.append(@name.getType())
        end
        for item in @items
            type_list.append(item.getType())
        end
    end
end
