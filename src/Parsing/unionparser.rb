require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'


class UnionParser
    def initialize()
        @keywords = getkeywords()
        @union_name = nil
        @item_name = nil
        @item_type = nil
        @itemList = Array.new()
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceUnion(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            unionNameStep(parser)
        else
            unexpectedToken(parser)
        end
        u = UnionStatement.new(@union_name, @itemList)
        reset()
        return u
    end

    def unionNameStep(parser)
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
        elsif(isValidIdentifier(peekTok))
            unionListItemStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def unionListItemStep(parser)
        token = parser.nextToken()
        @item_name = token
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        #elsif(peekTok.getType() == COMMA)
        #    commaStep(parser)
        #elsif(peekTok.getType() == ENDSCOPE)
         #   endStep(parser)
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
            unionListItemTypeStep(parser)
        else
            unexpectedToken(parser)
        end 
    end

    def unionListItemTypeStep(parser)
        token = parser.nextToken()
        @item_type = token
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
            addItemToList()
            unionListItemStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        addItemToList()
        parser.discard()
    end

    def addItemToList()
        @itemList.append(UnionItemListType.new(@item_name, @item_type))
        reset()
    end

    def reset()
        @union_name = nil
        @item_name = nil
        @item_type = nil
        @itemList = Array.new()
    end

    def enforceUnion(token)
        if(token.getText().upcase != UNION)
            throw Exception.new("Did not enounter \"union\" keyword in file " + token.getFilename())
        end
    end
end


class UnionItemListType
    def initialize(item_name, item_type)
        @item_name = item_name
        @item_type = item_type
    end

    def getName()
        return @item_name.getText()
    end

    def getType()
        return @item_type.getText()
    end
end

class UnionStatement
    def initialize(name, itemList)
        @union_name = name
        @items = itemList
    end

    def _printLiteral()
        astString = ""
        astString += "(name: " + @union_name.getText() + ", items: ["
        for item in @items do
            astString += item.getText() + ", "
        end
        astString = astString[0...-2] + "])"
        return astString
    end
end