require_relative '../keywords.rb'
require_relative '../tokentype.rb'
require_relative './token.rb'
require_relative '../Parsing/parserutilities.rb'


class Scanner 
    def initialize(charArrayScanner=nil) #char scanner for string interpolation
        @tokens = Array.new()
        @line = 1
        @filename = nil
        @keywords = getkeywords()
        @specialIdChars = ["@", "$", "_" , "~", "#", "&", ";", "?", "!"]
        if(charArrayScanner != nil)
            @charScanner = charArrayScanner
        else
            @charScanner = FileScanner.new()
        end
        @peekToken = nil
    end

    def reset()
        @tokens = Array.new()
        @peekToken = nil
        @filename = nil
        @line = 1
        @charScanner.reset()
    end

    def loadSource(filename)
        @charScanner.loadSource(filename)
        @filename = filename
        @line = 1
    end

    def closeSource
        @charScanner.closeSource()
        reset()
    end

    def bytesFromEnd()
        return @charScanner.bytesFromEnd()
    end

    def hasTokens
        return !isAtEnd()
    end

    def peekToken
        if(@peekToken != nil)
            return @peekToken
        end
        @peekToken = nextToken()
        return @peekToken
    end

    def nextToken
        if(@peekToken != nil)
            temp = @peekToken
            @peekToken = nil
            return temp
        end
        if(!isAtEnd())
            toklength = @tokens.length
            while(!isAtEnd() && toklength == @tokens.length)
                scanforToken()
            end
        else
            eof = Token.new(EOF, "", nil, @line, @filename)
            @tokens.append(eof)
        end
        temp = @tokens.pop()
        if temp == nil
            temp = Token.new(EOF, "", nil, @line, @filename)
        end
        return temp
    end

    def scanTokens
        while(!isAtEnd()) do
            scanforToken()
        end
        @tokens.append(Token.new(EOF, "", nil, @line, @filename))
        return @tokens
    end

    def scanforToken
        char = @charScanner.currentChar()
        @charScanner.setSliceStart()
        case char
        when "("
            addToken(LEFT_PAREN)
        when ")"
            addToken(RIGHT_PAREN)
        when ","
            addToken(COMMA)
        when "["
            addToken(LEFT_BRACKET)
        when "]"
            addToken(RIGHT_BRACKET)
        when "{"
            addToken(LEFT_BRACE)
        when "}"
            addToken(RIGHT_BRACE)
        when "?"
            addToken(QUESTION)
        when ":"
            addToken(COLON)
        when "."
            if(match("."))
                addToken(RANGE)
            else
                addToken(DOT)
            end
        when "="
            if(match("="))
                addToken(EQUAL_EQUAL)
            else
                addToken(EQUAL)
            end
        when "+"
            if(match("="))
                addToken(PLUS_EQUAL)
            else
                addToken(PLUS)
            end
        when "-"
            if(match("="))
                addToken(MINUS_EQUAL)
            else
                addToken(MINUS)
            end
        when "*"
            if(match("="))
                addToken(STAR_EQUAL)
            else
                addToken(STAR)
            end
        when "/"
            if(match("/"))
                while( @charScanner.currentChar() != "\n" and !isAtEnd())
                    @charScanner.shiftRight()
                end
                @charScanner.incCurrentIndex()
                @charScanner.shiftRight()
                @line += 1
            elsif(match("*"))
                multilineComment()
            elsif(match("="))
                addToken(SLASH_EQUAL)
            else
                addToken(SLASH)
            end
        when "^"
            if(match("="))
                addToken(CARROT_EQUAL)
            else
                addToken(CARROT)
            end
        when "%"
            if(match("="))
                addToken(MOD_EQUAL)
            else
                addToken(MOD)
            end
        when "!"
            if(match("="))
                addToken(BANG_EQUAL)
            else
                addToken(BANG)
            end
        when "<"
            if(match("="))
                addToken(LESS_EQUAL)
            else
                addToken(LESS)
            end
        when ">"
            if(match("="))
                addToken(GREATER_EQUAL)
            else
                addToken(GREATER)
            end
        when "%"
            if(match("="))
                addToken(MOD_EQUAL)
            else
                addToken(MOD)
            end
        when " ", "\t"
            @charScanner.shiftRight()
        when "\'"
            char()
        when "\""
            string()
        when "\r", "\n"
            @charScanner.incCurrentIndex()
            @charScanner.shiftRight()
            @line += 1
        else
            if(isDigit(char))
                number()
            elsif(isAlpha(char) or @specialIdChars.include?(char))
                identifier()
            else
                scanner_error("Unexpected character: #{char}")
            end
        end
        while(@charScanner.currentChar() in [" ", '\t', '\n', '\r'] and !isAtEnd())
            @charScanner.shiftRight()
        end
    end

    def identifier()
        while(isAlphaNumeric(peek()) or @specialIdChars.include?(peek()))
            @charScanner.shiftRight()
        end

        if(isGeneralKeyWord(@charScanner.getSlice()))
            addToken(@charScanner.getSlice().upcase)
        else
            addToken(IDENTIFIER)
        end
    end

    def number
        while(isDigit(peek()))
            @charScanner.shiftRight()
        end
        isfloat = false
        if(peek() == "." and isDigit(peekNext()))
            isfloat = true
            @charScanner.shiftRight()
            while(isDigit(peek()))
                @charScanner.shiftRight()
            end
        end

        if(isfloat)
            addToken(FLOAT)
        else
            addToken(INT)
        end
    end

    def isDigit(char)
        return ((char >= "0") and (char <= "9"))
    end

    def isAlpha(char)
        islowercase = (char.ord >= 'a'.ord && char.ord <= 'z'.ord)
        isuppercase = (char.ord >= 'A'.ord && char.ord <= 'Z'.ord)
        return (islowercase or isuppercase or char == '_')
    end

    def isAlphaNumeric(char)
        return (isAlpha(char) or isDigit(char))
    end

    def scanner_error(message)
        print "ERROR: In #{@filename} at #{(@line).to_s} \"" + message + "\""
    end

    def addToken(tok_type, literal = nil)
        text = @charScanner.getSlice()
        @tokens.append(Token.new(tok_type, text, literal, @line, @filename))
        @charScanner.shiftRight()
    end

    def isAtEnd
        return @charScanner.complete()
    end

    def match(expected)
        if(isAtEnd())
            return false
        end
        if(peek() != expected)
            return false
        end
        
        @charScanner.shiftRight()
        return true
    end

    def peek
        temp = @charScanner.peekChar()
        return temp
    end

    def peekNext
        temp = @charScanner.peekNextChar()
        return temp
    end

    def multilineComment
        comment_sections = 1
        @charScanner.shiftRight()

        while(!isAtEnd())
            while(@charScanner.currentChar() == " " and !isAtEnd())
                @charScanner.shiftRight()
            end

            current = @charScanner.currentChar()
            peek = @charScanner.peekChar()

            if(current == "/" and peek() == "*")
                comment_sections += 1
                @charScanner.shiftRight()
                @charScanner.shiftRight()
                current = @charScanner.currentChar()
            end

            if(current == "*" and peek() == "/")
                comment_sections -= 1
                @charScanner.shiftRight()
                

                _current = @charScanner.currentChar()
            end

            if(current == "\n" || current == "\r")
                @charScanner.incCurrentIndex()
                @line += 1
            end

            @charScanner.shiftRight()

            if(comment_sections == 0)
                break
            end
        end

        if(comment_sections > 0)
            print "line #{(@line).to_s} Unterminated block comment. #{comment_sections}"
        end
    end

    def char
        if(peek() == "\'")
            scanner_error("Empty character.")
        end
        @charScanner.shiftRight()
        if(peek() != "\'")
            scanner_error("Unterminated character.")
        end
        @charScanner.shiftRight()

        ch = @charScanner.getSlice()
        addToken(CHAR, ch)
    end

    def string
        while(peek() != "\"" and not isAtEnd())
            if(peek() == "\n")
                @line += 1
            end
            if(peek() == "\\")
                if(peekNext() == "\"")
                    @charScanner.shiftRight()
                end
            end

            @charScanner.shiftRight()
        end

        if(isAtEnd())
            scanner_error("Unterminated string.")
        end

        @charScanner.shiftRight()

        value = @charScanner.getSlice()
        addToken(STRING, value)
    end

end





class FileScanner

    def initialize
        @source = nil
        @current = 1
        @filesize = nil
        @SliceIdx = 1
    end

    def reset()
        @source = nil
        @current = 1
        @filesize = nil
        @SliceIdx = 1
    end

    def getFilesize
        return @filesize
    end

    def bytesFromEnd()
        return @filesize - @current
    end

    def getCurrent
        return @current
    end

    def loadSource(filename)
        @source = File.open(filename)
        @filesize = @source.size() 
    end

    def printSource
        while !@source.eof?()
            puts @source.sysread(1)
        end
    end

    def closeSource
        @source.close()
        reset()
    end

    def readChar
        if(complete())
            return '\0'
        end
        char = @source.sysread(1)
        @current += 1
        return char
    end

    def peekChar
        if(@current + 1 > @filesize)
            return '\0'
        end
        char = readChar()
        @current -= 1
        char = readChar()
        if(char == "\r" or char == "\n")
            @source.seek(-1, IO::SEEK_CUR)
        end
        @current -= 1
        @source.seek(-2, IO::SEEK_CUR)
        return char
    end

    def peekNextChar
        if(@current + 2 > @filesize)
            return '\0'
        end
        char = readChar()
        if(char == "\r" or char == "\n")
            # "char is a newline"
            @source.seek(-1, IO::SEEK_CUR)
        end
        @current -= 1
        char = readChar()
        if(char == "\r" or char == "\n")
            @source.seek(-1, IO::SEEK_CUR)
        end
        @current -= 1
        char = readChar()
        @current -= 1
        @source.seek(-3, IO::SEEK_CUR)
        return char
    end

    def currentChar
        if(complete())
            return '\0'
        end
        current = readChar()
        @current -= 1
        @source.seek(-1, IO::SEEK_CUR)
        return current
    end

    def incCurrentIndex
        @current += 1
    end

    def shiftRight
        readChar()
    end

    def setSliceStart
        @SliceIdx = @current
    end

    def getSlice
        tempcurrent = @current
        slice_size = (@current - @SliceIdx) + 1 # includes chr at current
        @current -= (slice_size - 1)
        if(slice_size == 1)
            slice = readChar()
            if(!complete())
                @source.seek(-1, IO::SEEK_CUR)
                @current -= 1
            end
            return slice
        end

        @source.seek(-(slice_size - 1), IO::SEEK_CUR)
        token = ""
        for i in 1 .. slice_size do
            if(complete())
                break
            end
            token += readChar()
            @current -= 1
        end
        @source.seek(-1, IO::SEEK_CUR)
        @current = tempcurrent
        
        return token
    end

    def complete
        return ((@current > @filesize) or @source.eof?) 
    end
end