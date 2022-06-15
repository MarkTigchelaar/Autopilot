require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/import_statement.rb'

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
