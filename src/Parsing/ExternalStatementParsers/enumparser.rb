require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../Tokenization/token.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/enum_statement.rb'

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
        elsif(isFloat(peekTok))
            itemListLiteralStep(parser)
        elsif(is_boolean_keyword(peekTok))
            itemListLiteralStep(parser)
        elsif(is_string_or_char(peekTok))
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
