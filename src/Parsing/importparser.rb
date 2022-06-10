require_relative './parserutilities.rb'
require_relative '../tokentype.rb'

class ImportParser

    def initialize()
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
        ERRORS::addError(parser, msg)
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
            @moduleName = name
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
        ERRORS::addError(parser, msg)
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

    def toJSON()
        return {
            "type" => "module",
            "name" => {
                "literal" => @modulename.getText(),
                "type" => @modulename.getType(),
                "line_number" => @modulename.getLine()
            },
            "import_list" => getImportListJSON(),
            "is_library" => @isLibrary
        }
    end

    def getImportListJSON()
        items = Array.new()
        for item in @itemList
            items.append({
                "literal" => item.getText(),
                "type" => item.getType(),
                "line_number" => item.getLine()
            })
        end
        return items
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
        return "name:#{@modulename.getText()} type:#{libormod} items:[#{items}]"
    end

    def _printTokType(item_list)
        for item in @itemList
            item_list.append(item.getType())
        end
    end
end