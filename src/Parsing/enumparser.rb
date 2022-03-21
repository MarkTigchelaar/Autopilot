require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/token.rb'

class EnumParser
    def initialize()
        @keywords = getkeywords()
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
        end
        e = enumStatement()
        reset()
        return e
    end

    def enumNameStep(parser)
        peekTok = parser.peek()
        @name = peekTok
        #puts @name.getText() + "--------------------------"
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
        end
    end

    def isStep(parser)
        parser.discard()
        peekTok = parser.peek()
        #puts "In isStep -----------------------------------"
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            itemListStep(parser)
        else
            invalidItemName(parser)
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
        else
            invalidItemName(parser)
        end
    end

    def enumTypeStep(parser)
        peekTok = parser.peek()
        @generaltype = peekTok
        #puts "                         Current item: #{peekTok.getText()}"
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            closeParenForEnumStep(parser)
        else
            unexpectedToken(parser)
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
        end
    end

    def itemListStep(parser)

        #puts "                              In itemListStep"
        peekTok = parser.peek()
        @currentItemName = peekTok
        #puts "current item name: #{@currentItemName.getText()}"
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
            #puts "Found end scope, adding list item"
            addToItemList()
            endStep(parser)
        else
            invalidItemName(parser)
        end
    end

    def commaStep(parser)
       #puts "in comma step"
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            itemListStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def equalStep(parser)
      # puts "                                    In equal Step"
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
           #puts "In equal step, found identifier"
            itemListLiteralStep(parser)
        elsif(isNumeric(peekTok))
           #puts "In equal step, found number"
            # tokenizer splits text on '.'
            # floats will be 3 tokens total
            itemListLiteralStep(parser)
        else
            #puts "unexpected token: #{peekTok.getText()}"
            unexpectedToken(parser)
        end
    end

    def itemListLiteralStep(parser)
       #puts "itemListLiteralStep"
        @currentItemLiteralToken = getNumberOrToken(parser)
        #puts "current item literal token: #{@currentItemLiteralToken.getText()}"
        #parser.discard()
        peekTok = parser.peek()
        #puts "next peek Token: #{peekTok.getText()}, #{peekTok.getType()}"
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == COMMA)
           #puts "found comma"
            addToItemList()
            commaStep(parser)
        elsif(peekTok.getText() == ENDSCOPE)
            addToItemList()
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def getNumberOrToken(parser)
       #puts "getNumberOrToken"
        current = parser.peek()
        if(!isNumeric(current))
            #puts "not numeric, returning current"
            return parser.nextToken()
        end
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getText() != '.')
           #puts "returning current"
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
               #puts "in nested else"
                unexpectedToken(parser)
            end
            parser.discard()
            return Token.new(current.getType(), txt, txt, current.getLine(), current.getFilename())
        end
    end

    def endStep(parser)
        parser.discard()
        #peekTok = parser.peek()
        #if(isEOF(peekTok))
        #    eofReached(parser)
        #end
    end

    def addToItemList()
        @itemList.append(
            EnumListItem.new(
                @currentItemName,
                @currentItemLiteralToken
            )
        )

=begin
       #puts "Item information:"
        if @currentItemName != nil
           #puts "  name: #{@currentItemName.getText()}"
        else
           #puts "  name is nil"
        end
        if @currentItemLiteralToken != nil
           #puts "  literal: #{@currentItemLiteralToken.getText()}"
        else
           #puts "  literal is nil"
        end
=end
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

    def invalidItemName(parser)
        msg = "Invalid name for item #{parser.peek().getText()}."
        addError(parser, msg)
    end

    def unexpectedToken(parser)
        msg = "Unexpected token #{parser.peek().getText()}."
        addError(parser, msg)
    end

    def isEOF(token)
        return token.getType() == EOF
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

    def addError(parser, message)
       #puts "ADDING ERROR"
        parser.addError(parser.nextToken(), message)
        parser.setToSync()
        reset()
    end

    def eofReached(parser)
        msg = "End of file reached."
        addError(parser, msg)
    end

    def enumStatement()
        #puts @name.getText() + "]]]]]"
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

    def getName()
        return @name.getText()
    end

    def getType()
        # type of enum, not the type of the token
        if @type != nil
            return @type.getText()
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
end

class EnumStatement
    def initialize(name, itemList, generaltype)
        @name = name
        #puts @name.getText() + "--===="
        @items = itemList
        @enumtype = generaltype
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
end
