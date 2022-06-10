require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../Tokenization/token.rb'

class EnumParser
    def initialize()
        @name = nil
        @generaltype = nil
        @itemList = Array.new
        @currentItemName = nil
        @currentItemLiteralToken = nil
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceEnum(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            enumNameStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
        e = enumStatement()
        reset()
        return e
    end

    def enumNameStep(parser)
        peekTok = parser.peek()
        @name = peekTok
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IS)
            isStep(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            openParenForEnumStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
    end

    def isStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            itemListStep(parser)
        else
            invalidItemName(parser)
            reset()
        end
    end

    def openParenForEnumStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            enumTypeStep(parser)
        elsif(isPrimitiveType(peekTok))
            enumTypeStep(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            unexpectedToken(parser)
            reset()
        else
            invalidItemName(parser)
            reset()
        end
    end

    def enumTypeStep(parser)
        peekTok = parser.peek()
        @generaltype = peekTok
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            closeParenForEnumStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
    end

    def closeParenForEnumStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == IS)
            isStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
    end

    def itemListStep(parser)
        peekTok = parser.peek()
        @currentItemName = peekTok
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            addToItemList()
            commaStep(parser)
        elsif(peekTok.getType() == EQUAL)
            equalStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            addToItemList()
            endStep(parser)
        else
            invalidItemName(parser)
            reset()
        end
    end

    def commaStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            itemListStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
    end

    def equalStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            itemListLiteralStep(parser)
        elsif(isNumeric(peekTok))
            # tokenizer splits text on '.'
            # floats will be 3 tokens total
            itemListLiteralStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
    end

    def itemListLiteralStep(parser)
        @currentItemLiteralToken = getNumberOrToken(parser)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
            addToItemList()
            commaStep(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            addToItemList()
            endStep(parser)
        else
            unexpectedToken(parser)
            reset()
        end
    end

    def getNumberOrToken(parser)
        current = parser.peek()
        if(!isNumeric(current))
            return parser.nextToken()
        end
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getText() != '.')
            return current
        else
            middle = peekTok
            parser.discard()
            peekTok = parser.peek()
            txt = ""
            if(isEOF(peekTok))
                eofReached(parser)
            elsif(isNumeric(peekTok))
                txt = current.getText() + middle.getText() + peekTok.getText()
            else
                unexpectedToken(parser)
                reset()
            end
            parser.discard()
            return Token.new(current.getType(), txt, txt, current.getLine(), current.getFilename())
        end
    end

    def endStep(parser)
        parser.discard()
    end

    def addToItemList()
        @itemList.append(
            EnumListItem.new(
                @currentItemName,
                @currentItemLiteralToken
            )
        )
        resetCurrentItems()
    end

    def resetCurrentItems()
        @currentItemName = nil
        @currentItemLiteralToken = nil
    end

    def reset()
        @name = nil
        @generaltype = nil
        @itemList = Array.new
        resetCurrentItems()
    end

    def enumStatement()
        enum = EnumStatement.new(@name, @itemList, @generaltype)
        reset()
        return enum
    end

    def enforceEnum(token)
        if(token.getText().upcase != ENUM)
            throw Exception.new("Did not enounter \"enum\" keyword in file " + token.getFilename())
        end
    end
end


class EnumListItem
    def initialize(name, default_value_token)
        @name = name
        @default_value_token = default_value_token
    end

    def toJSON()
        default_literal = ""
        default_literal = @default_value_token.getText() if @default_value_token != nil
        default_value = ""
        default_value = @default_value_token.getType() if @default_value_token != nil

        return {
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType()
            },
            "default_value" => {
                "literal" => default_literal,
                "type" => default_value
            }
        }
    end

    def getName()
        return @name.getText()
    end

    def getType()
        # type of enum, not the type of the token
        if @name != nil
            return @name.getType()
        else
            return "null"
        end
    end

    def getDefaultValue()
        if @default_value_token != nil
            return @default_value_token.getText()
        else
            return "null"
        end
    end

    def getDefaultValueType()
        if @default_value_token != nil
            return @default_value_token.getType()
        else
            return "NULL"
        end
    end
end

class EnumStatement
    def initialize(name, itemList, generaltype)
        @name = name
        @items = itemList
        @enumtype = generaltype
    end

    def toJSON()
        type_lit = ""
        type_lit = @enumtype.getText() if @enumtype
        type_type = ""
        type_type = @enumtype.getType() if @enumtype
        line = ""
        line = @enumtype.getLine() if @enumtype
        return {
            "type" => "enum",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "fields" => getItemsJSON(),
            "enumtype" => {
                "literal" => type_lit,
                "type" => type_type,
                "line_number" => line
            }
        }
    end

    def getItemsJSON()
        itemList = Array.new()
        for item in @items
            itemList.append(item.toJSON())
        end
        return itemList
    end

    def _printLiteral()
        ename = "null"
        if @name != nil
            ename = @name.getText()
        end
        enumtype = "null"
        if @enumtype != nil
            enumtype = @enumtype.getText()
        end
        astJSON = "("
        
        astJSON += "name" + " : " + ename + ", "
        astJSON += "type" + " : " + enumtype + ", "
        astJSON += "items" + " : ["
        for item in @items do
            astJSON += printItem(item) + ", "
        end
        astJSON = astJSON[0...-2]
        return astJSON + "])"
    end

    def printItem(item)
        itemString = ""
        itemString += "(name : " + item.getName() + ", "
        itemString += "default_value" + " : " + item.getDefaultValue()
        itemString += ")"
        return itemString
    end

    def _printTokType(item_list)
        item_list.append(@name.getType())
        if(@enumtype != nil)
            item_list.append(@enumtype.getType())
          end
        for item in @items do
            item_list.append(item.getType().upcase)
            item_list.append(item.getDefaultValueType())
        end
    end
end
