require_relative './parserutilities.rb'
require_relative '../tokentype.rb'
require_relative '../keywords.rb'

class ImportParser

    def initialize()
        @keywords = getkeywords()
        @itemList = Array.new
        @isLibrary = false
        @moduleName = ""
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceImport(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == MODULE)
            moduleStep(parser)
        elsif(peekTok.getType() == LIBRARY)
            libraryStep(parser)
        elsif(isValidIdentifier(peekTok))
            itemListStep(parser)
        else
            invalidItemName(parser)
        end
        result = ImportStatement.new(@moduleName, @itemList, @isLibrary)
        reset()
        return result
    end

    def enforceImport(peekTok)
        if(peekTok.getText().upcase != IMPORT)
            throw Exception.new("Did not enounter \"import\" keyword in file " + peekTok.getFilename())
        end
    end


    def eofReached(parser)
        msg = "End of file reached."
        addError(parser, msg)
    end

    def moduleStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isKeyword(peekTok))
            invalidModuleName(parser)
        elsif(!isAlphaNumericWord(peekTok))
            invalidModuleName(parser)
        else
            moduleNameStep(parser)
        end
    end

    def libraryStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isKeyword(peekTok))
            invalidModuleName(parser)
        elsif(!isAlphaNumericWord(peekTok))
            invalidModuleName(parser)
        else
            @isLibrary = true
            moduleNameStep(parser)
        end
    end

    def moduleNameStep(parser)
        name = parser.nextToken()
        if(!isValidIdentifier(name))
            invalidModuleName(parser)
        else
            @moduleName = name.getText()
        end
    end

    def itemListStep(parser)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        end
        @itemList.append(peekTok)
        parser.discard()
        peekTok = parser.peek()
        if(peekTok.getType() == FROM)
            fromStep(parser)
        elsif(peekTok.getType() == COMMA)
            commaStep(parser)
        elsif(isEOF(peekTok))
            eofReached(parser)
        else
            unexpectedToken(parser)
        end   
    end

    def fromStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == MODULE)
            moduleStep(parser)
        elsif(peekTok.getType() == LIBRARY)
            libraryStep(parser)
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
            itemListStep(parser)
        elsif(isKeyword(peekTok))
            invalidItemName(parser)
        else
            unexpectedToken(parser)
        end
    end

    def invalidModuleName(parser)
        msg = "Invalid module or library name #{parser.peek().getText()}."
        addError(parser, msg)
    end

    def invalidItemName(parser)
        msg = "Invalid name for imported item #{parser.peek().getText()}."
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
        parser.addError(parser.nextToken(), message)
        parser.setToSync()
        reset()
    end

    def reset()
        @moduleName = ""
        @itemList = Array.new
        @isLibrary = false
    end
end

class ImportStatement
    def initialize(modulename, itemList, isLibrary)
        @modulename = modulename
        @itemList = itemList
        @isLibrary = isLibrary
    end

    def _printLiteral
        libormod = "mod"
        if(@isLibrary)
            libormod = "lib"
        end
        items = ""
        for item in @itemList
            items += item + ","
        end
        if(items[-1] == ',')
            items = items[0 .. -1]
        end
        if(items == "")
            items = "none"
        end
        return "name:#{@modulename} type:#{libormod} items:[#{items}]"
    end
end